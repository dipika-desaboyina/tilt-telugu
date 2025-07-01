import pandas as pd
import regex as re

def extract_telugu_sentences(paragraph, min_words=15):
    """
    Extract Telugu-only sentences from a paragraph.
    Filters out English and short sentences.
    """
    if not isinstance(paragraph, str):
        return []

    raw_sentences = re.split(r'[।.!?]', paragraph)

    cleaned = []
    for sentence in raw_sentences:
        words = sentence.split()
        telugu_words = [word for word in words if re.search(r'\p{Telugu}', word)]
        if len(telugu_words) >= min_words:
            cleaned.append(' '.join(telugu_words).strip())

    return cleaned

def main():
    input_path = "/home/jellybun/Downloads/telugu_web-scraped_code-mixed_text (1).xlsx" 
    output_path = "/home/jellybun/Downloads/telugu_cleaned_sentences.csv"

    df = pd.read_excel(input_path)

    structured_rows = []

    for _, row in df.iterrows():
        sentences = extract_telugu_sentences(row['text'])

        for sentence in sentences:
            row_dict = row.to_dict()
            row_dict['telugu_sentence'] = sentence
            structured_rows.append(row_dict)

    out_df = pd.DataFrame(structured_rows)

    cols = ['telugu_sentence'] + [col for col in out_df.columns if col != 'telugu_sentence']
    out_df = out_df[cols]

    out_df.to_csv(output_path, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()
