import torch
from transformers import BertTokenizer, BertForQuestionAnswering

# ✅ Load from local or huggingface
model_path = "./chatbot/bert_squad_model"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForQuestionAnswering.from_pretrained(model_path)

# ✅ Use CPU by default (you can also set to 'cuda' if you have GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
model.eval()

def question_answer(question, context):
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

    # Get the most likely start and end positions
    start_idx = torch.argmax(start_scores, dim=1).item()
    end_idx = torch.argmax(end_scores, dim=1).item()

    # Decode answer
    all_tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    answer_tokens = all_tokens[start_idx : end_idx + 1]
    answer = tokenizer.convert_tokens_to_string(answer_tokens)

    return answer
