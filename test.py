from transformers import BertForSequenceClassification, BertTokenizer

# Load pre-trained model and tokenizer
model_name = "bert-base-multilingual-cased"
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Example text from the next thesis first page
text_next = """
[Text from the next first page of the thesis]
"""

# Tokenize the text
inputs_next = tokenizer(text_next, return_tensors="pt", truncation=True)

# Use the model to extract the title
outputs_next = model(**inputs_next)

# Get the predicted label
predicted_label = outputs_next.logits.argmax().item()

# Convert the label to text using the tokenizer
extracted_title = tokenizer.decode(predicted_label)

# Print the extracted title
print("Extracted Title from the Next Thesis First Page:", extracted_title)
from transformers import BertForSequenceClassification, BertTokenizer

# Load pre-trained model and tokenizer
model_name = "bert-base-multilingual-cased"
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Example text from the next thesis first page
text_next = """
[Text from the next first page of the thesis]
"""

# Tokenize the text
inputs_next = tokenizer(text_next, return_tensors="pt", truncation=True)

# Use the model to extract the title
outputs_next = model(**inputs_next)

# Get the predicted label
predicted_label = outputs_next.logits.argmax().item()

# Convert the label to text using the tokenizer
extracted_title = tokenizer.decode(predicted_label)

# Print the extracted title
print("Extracted Title from the Next Thesis First Page:", extracted_title)
