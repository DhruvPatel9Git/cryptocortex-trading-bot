from transformers import BertTokenizer, BertForQuestionAnswering

model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForQuestionAnswering.from_pretrained(model_name)

tokenizer.save_pretrained("./bert_squad_model")
model.save_pretrained("./bert_squad_model")
