import pandas as pd
import json
import re
from typing import List, Dict
import random

class UnifiedDatasetBuilder:
    
    def __init__(self):
        self.unified_data = []
        self.stats = {
            'medical': 0,
            'therapy': 0,
            'emotion': 0,
            'nutrition': 0
        }
    
    def process_medical_dataset(self, df: pd.DataFrame) -> List[Dict]:

        instructions = []
        
        for _, row in df.iterrows():
            med_name = str(row['Medicine Name']).strip()
            composition = str(row['Composition']).strip()
            uses = str(row['Uses']).strip()
            side_effects = str(row['Side_effects']).strip()
            manufacturer = str(row['Manufacturer']).strip()
            
            
            # general medication information
            instructions.append({
                "instruction": f"What is {med_name} and what is it used for?",
                "input": "",
                "output": f"{med_name} contains {composition}. It is used to treat: {uses}. Common side effects include {side_effects}. This medication is manufactured by {manufacturer}.",
                "category": "medical",
                "subcategory": "medication_info"
            })
            
            # side effects inquiry
            if side_effects != 'nan' and len(side_effects) > 0:
                instructions.append({
                    "instruction": f"What are the side effects of {med_name}?",
                    "input": "",
                    "output": f"Common side effects of {med_name} include: {side_effects}. If you experience severe symptoms, consult your healthcare provider immediately.",
                    "category": "medical",
                    "subcategory": "side_effects"
                })
            
            # composition inquiry
            if composition != 'nan' and len(composition) > 0:
                instructions.append({
                    "instruction": f"What is the active ingredient in {med_name}?",
                    "input": "",
                    "output": f"The active ingredient(s) in {med_name} are: {composition}.",
                    "category": "medical",
                    "subcategory": "composition"
                })
            
            # usage context
            if uses != 'nan' and len(uses) > 0:
                instructions.append({
                    "instruction": f"When should I take {med_name}?",
                    "input": "",
                    "output": f"{med_name} is prescribed for {uses}. Always follow your doctor's instructions regarding dosage and timing.",
                    "category": "medical",
                    "subcategory": "usage"
                })
            
            # alternative phrasing for variety
            instructions.append({
                "instruction": "I was prescribed {}, can you tell me about it?".format(med_name),
                "input": "",
                "output": f"Certainly! {med_name} is a medication containing {composition}. It's commonly used for {uses}. Be aware of potential side effects such as {side_effects}.",
                "category": "medical",
                "subcategory": "medication_info"
            })
        
        self.stats['medical'] = len(instructions)
        return instructions
    
    def process_therapy_dataset(self, df: pd.DataFrame) -> List[Dict]:
        instructions = []
        
        for _, row in df.iterrows():
            try:
                conv_str = row['conversations']
                
                # clean up
                conv_str = conv_str.strip('"\'')
                
                # fix double double quotes
                conv_str = re.sub(r'\}\s+\{', '}, {', conv_str)
                conv_str = conv_str.replace('""', '"')
                
                try:
                    conversation = eval(conv_str)
                except Exception as e:
                    print(f"parsing error: {str(e)[:80]}")
                    continue
                
                # extract human-ai pairs
                for i in range(len(conversation)):
                    if conversation[i].get('from') == 'human':
                        human_msg = conversation[i].get('value', '')
                        
                        if i + 1 < len(conversation) and conversation[i + 1].get('from') == 'gpt':
                            gpt_msg = conversation[i + 1].get('value', '')
                            
                            if human_msg and gpt_msg:
                                instructions.append({
                                    "instruction": "Provide empathetic therapeutic support.",
                                    "input": human_msg,
                                    "output": gpt_msg,
                                    "category": "therapy",
                                    "subcategory": "conversation"
                                })
                        
            except Exception as e:
                print(f"Error processing therapy conversation row: {str(e)[:80]}")
                continue
        
        self.stats['therapy'] = len(instructions)
        return instructions
    
    def process_emotion_dataset(self, df: pd.DataFrame) -> List[Dict]:
        instructions = []
        
        # emotion-response mapping
        emotion_responses = {
            'fear': "I can sense you're feeling anxious or afraid. It's completely normal to have these feelings. Would you like to talk about what's causing this anxiety?",
            'sad': "I hear that you're feeling down. Those feelings are valid and it's okay to feel this way. What's been weighing on your mind?",
            'anger': "It sounds like you're feeling frustrated or angry. Let's work through this together. What happened that made you feel this way?",
            'joy': "I'm glad to hear you're feeling positive! It's wonderful to experience joy. What's bringing you happiness today?",
            'love': "It's beautiful to feel connected and caring. Those emotions are precious. Tell me more about what you're experiencing.",
            'surprise': "That must have been unexpected! How are you processing this? Sometimes surprises can bring mixed feelings.",
            'suprise': "That must have been unexpected! How are you processing this? Sometimes surprises can bring mixed feelings.",  # Handle typo in dataset
            'neutral': "I'm here to listen. What's on your mind today?",
            'disgust': "It sounds like something has really bothered you. It's okay to feel uncomfortable about certain things. Can you tell me more?",
            'shame': "I understand you're experiencing difficult emotions. Please know that everyone makes mistakes and has struggles. You're not alone in this.",
            'guilt': "Feelings of guilt can be heavy to carry. It's important to remember that recognizing these feelings is the first step. Would you like to talk about it?"
        }
        
        for _, row in df.iterrows():
            sentence = str(row['sentence']).strip()
            emotion = str(row['emotion']).strip().lower()
            
            if sentence == 'nan' or len(sentence) < 5:
                continue
            
            # Template 1: emotion detection
            instructions.append({
                "instruction": "Identify the emotional tone in this message.",
                "input": sentence,
                "output": f"The person appears to be feeling {emotion}.",
                "category": "emotion",
                "subcategory": "detection"
            })
            
            # Template 2: empathetic response
            response = emotion_responses.get(emotion, emotion_responses['neutral'])
            
            instructions.append({
                "instruction": "Respond empathetically to this message.",
                "input": sentence,
                "output": response,
                "category": "emotion",
                "subcategory": "empathy"
            })
            
            # Template 3: emotional validation
            instructions.append({
                "instruction": "Provide emotional validation and support.",
                "input": sentence,
                "output": f"I understand you're feeling {emotion}. Your emotions are valid, and it's important to acknowledge them. {response}",
                "category": "emotion",
                "subcategory": "validation"
            })
        
        self.stats['emotion'] = len(instructions)
        return instructions
    
    def process_nutrition_dataset(self, df: pd.DataFrame) -> List[Dict]:

        instructions = []
        
        for _, row in df.iterrows():
            food_name = str(row['Shrt_Desc']).strip()
            
            # nutritional values
            def safe_float(val, default=0.0):
                try:
                    return float(val) if pd.notna(val) else default
                except:
                    return default
            
            calories = safe_float(row['Energ_Kcal'])
            protein = safe_float(row['Protein_(g)'])
            fat = safe_float(row['Lipid_Tot_(g)'])
            carbs = safe_float(row['Carbohydrt_(g)'])
            fiber = safe_float(row['Fiber_TD_(g)'])
            calcium = safe_float(row['Calcium_(mg)'])
            iron = safe_float(row['Iron_(mg)'])
            sodium = safe_float(row['Sodium_(mg)'])
            
            if food_name == 'nan' or len(food_name) < 2:
                continue
            
            # Template 1: nutritional content overview
            instructions.append({
                "instruction": f"What is the nutritional content of {food_name}?",
                "input": "",
                "output": f"{food_name} contains approximately {calories:.0f} kcal per 100g, with {protein:.1f}g protein, {fat:.1f}g fat, and {carbs:.1f}g carbohydrates. It also provides {fiber:.1f}g of dietary fiber.",
                "category": "nutrition",
                "subcategory": "content"
            })
            
            # Template 2: caloric information
            instructions.append({
                "instruction": f"How many calories are in {food_name}?",
                "input": "",
                "output": f"{food_name} contains approximately {calories:.0f} calories per 100g serving.",
                "category": "nutrition",
                "subcategory": "calories"
            })
            
            # Template 3: macronutrient breakdown
            instructions.append({
                "instruction": f"What are the macronutrients in {food_name}?",
                "input": "",
                "output": f"{food_name} has {protein:.1f}g protein, {fat:.1f}g fat, and {carbs:.1f}g carbohydrates per 100g.",
                "category": "nutrition",
                "subcategory": "macros"
            })
            
            # Template 4: high-protein recommendation
            if protein > 15:
                instructions.append({
                    "instruction": "Recommend a high-protein food.",
                    "input": "I need to increase my protein intake for muscle building.",
                    "output": f"I recommend {food_name}, which contains {protein:.1f}g of protein per 100g. It's an excellent source of protein for muscle growth and recovery.",
                    "category": "nutrition",
                    "subcategory": "recommendation"
                })
            
            # Template 5: low-calorie recommendation
            if calories < 100 and calories > 20:
                instructions.append({
                    "instruction": "Suggest a low-calorie food option.",
                    "input": "I'm trying to lose weight. What are some low-calorie foods?",
                    "output": f"{food_name} is a great low-calorie option with only {calories:.0f} calories per 100g. It can help you maintain a caloric deficit while still getting nutrients.",
                    "category": "nutrition",
                    "subcategory": "recommendation"
                })
            
            # Template 6: micronutrient information
            if calcium > 100 or iron > 2:
                micronutrients = []
                if calcium > 100:
                    micronutrients.append(f"{calcium:.0f}mg calcium")
                if iron > 2:
                    micronutrients.append(f"{iron:.1f}mg iron")
                
                instructions.append({
                    "instruction": f"What micronutrients does {food_name} provide?",
                    "input": "",
                    "output": f"{food_name} is a good source of {', '.join(micronutrients)}, which are important for bone health and oxygen transport in the body.",
                    "category": "nutrition",
                    "subcategory": "micronutrients"
                })
            
            # Template 7: sodium content
            if sodium > 500:
                instructions.append({
                    "instruction": f"Is {food_name} high in sodium?",
                    "input": "",
                    "output": f"Yes, {food_name} contains {sodium:.0f}mg of sodium per 100g, which is relatively high. If you're watching your sodium intake, consume this in moderation.",
                    "category": "nutrition",
                    "subcategory": "sodium"
                })
        
        self.stats['nutrition'] = len(instructions)
        return instructions
    
    def merge_all(self, medical_df: pd.DataFrame,
                  therapy_df: pd.DataFrame,
                  emotion_df: pd.DataFrame,
                  nutrition_df: pd.DataFrame,
                  shuffle: bool = True) -> pd.DataFrame:
        """
        MERGE
        """
        print("=" * 60)
        print("PROCESSING DATASETS FOR QLORA FINE-TUNING")
        print("=" * 60)
        
        print("\n[1/4] Processing medical dataset...")
        medical_instructions = self.process_medical_dataset(medical_df)
        print(f"      Generated {len(medical_instructions)} instruction pairs")
        
        print("\n[2/4] Processing therapy dataset...")
        therapy_instructions = self.process_therapy_dataset(therapy_df)
        print(f"      Generated {len(therapy_instructions)} instruction pairs")
        
        print("\n[3/4] Processing emotion dataset...")
        emotion_instructions = self.process_emotion_dataset(emotion_df)
        print(f"      Generated {len(emotion_instructions)} instruction pairs")
        
        print("\n[4/4] Processing nutrition dataset...")
        nutrition_instructions = self.process_nutrition_dataset(nutrition_df)
        print(f"      Generated {len(nutrition_instructions)} instruction pairs")
        
        all_instructions = (medical_instructions + 
                          therapy_instructions + 
                          emotion_instructions + 
                          nutrition_instructions)
        
        print(f"\n{'=' * 60}")
        print(f"TOTAL INSTRUCTION PAIRS: {len(all_instructions)}")
        print(f"{'=' * 60}")
        
        if shuffle:
            print("\n[Shuffling dataset for better training distribution...]")
            random.seed(42) # seed
            random.shuffle(all_instructions)
        
        # dataframe
        unified_df = pd.DataFrame(all_instructions)
        
        return unified_df
    
    def print_statistics(self, df: pd.DataFrame):
        """STATS"""
        print("\n" + "=" * 60)
        print("DATASET STATISTICS")
        print("=" * 60)
        print(f"\nTotal samples: {len(df):,}")
        
        print(f"\n{'Category Distribution:'}")
        print("-" * 40)
        category_counts = df['category'].value_counts()
        for cat, count in category_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {cat.capitalize():12} {count:6,} ({percentage:5.1f}%)")
        
        print(f"\n{'Subcategory Breakdown:'}")
        print("-" * 40)
        for category in df['category'].unique():
            print(f"\n  {category.upper()}:")
            subcat_counts = df[df['category'] == category]['subcategory'].value_counts()
            for subcat, count in subcat_counts.items():
                print(f"    - {subcat:20} {count:6,}")
        
        print(f"\n{'=' * 60}")
    
    def save_for_qlora(self, df: pd.DataFrame, output_path: str = "unified_dataset.jsonl"):
        """
        JSONL Alpaca format
        """
        print(f"\n[Saving to {output_path}...]")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for _, row in df.iterrows():
                sample = {
                    "instruction": row['instruction'],
                    "input": row['input'],
                    "output": row['output']
                }
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')
        
        print(f"Saved {len(df):,} samples to {output_path}")
        
        # metadata for analysis
        metadata_path = output_path.replace('.jsonl', '_with_metadata.csv')
        df.to_csv(metadata_path, index=False)
        print(f"Saved metadata version to {metadata_path}")
        
        # samples
        sample_path = output_path.replace('.jsonl', '_sample.json')
        with open(sample_path, 'w', encoding='utf-8') as f:
            sample_data = df.head(20).to_dict('records')
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        print(f"Saved sample preview (20 entries) to {sample_path}")



def main():    
    medical_df = pd.read_csv("datasets/med_1.csv")
    print(f"  Medical: {len(medical_df)} rows")
    
    therapy_conversations = []
    therapy_ids = []
    
    with open("datasets/theurapetic_sessions_3.csv", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        current_conv = ""
        current_id = ""
        in_conversation = False
        
        for line in lines[1:]:
            if line.strip().startswith('"[{'):
                if current_conv:
                    therapy_conversations.append(current_conv)
                    therapy_ids.append(current_id)
                current_conv = line.strip()
                in_conversation = True
            elif in_conversation:
                current_conv += " " + line.strip()
                if '",identity_' in line or '\",identity_' in line:
                    parts = current_conv.split(',identity_')
                    if len(parts) == 2:
                        current_conv = parts[0].strip('"')
                        current_id = 'identity_' + parts[1].strip()
                        therapy_conversations.append(current_conv)
                        therapy_ids.append(current_id)
                        current_conv = ""
                        current_id = ""
                        in_conversation = False
        
        if current_conv:
            therapy_conversations.append(current_conv)
            therapy_ids.append(current_id if current_id else f'identity_{len(therapy_conversations)-1}')
    
    therapy_df = pd.DataFrame({'conversations': therapy_conversations, 'id': therapy_ids})
    print(f"  Therapy: {len(therapy_df)} rows")
    
    emotion_df = pd.read_csv("datasets/emotions_2.csv")
    print(f"  Emotion: {len(emotion_df)} rows")
    
    nutrition_df = pd.read_csv("datasets/nutritionalData_4.csv")
    print(f"  Nutrition: {len(nutrition_df)} rows")
    
    # init
    builder = UnifiedDatasetBuilder()
    
    unified_df = builder.merge_all(
        medical_df=medical_df,
        therapy_df=therapy_df,
        emotion_df=emotion_df,
        nutrition_df=nutrition_df,
        shuffle=True
    )
    
    # stats
    builder.print_statistics(unified_df)
    
    # save
    builder.save_for_qlora(unified_df, "unified_health_coach_dataset.jsonl")
    
    # 90 10 split
    print("\n" + "=" * 60)
    print("CREATING TRAIN/VALIDATION SPLIT")
    print("=" * 60)
    
    train_size = int(0.9 * len(unified_df))
    train_df = unified_df[:train_size]
    val_df = unified_df[train_size:]
    
    builder.save_for_qlora(train_df, "train.jsonl")
    builder.save_for_qlora(val_df, "val.jsonl")
    
    print(f"\n  Train set: {len(train_df):,} samples (90%)")
    print(f"  Validation set: {len(val_df):,} samples (10%)")


if __name__ == "__main__":
    main()