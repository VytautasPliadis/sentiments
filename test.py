def clean_titles(input_text):
    try:
        cleaned_text = input_text.split(' / \n', 1)[1]
    except:
        cleaned_text = input_text.split('\r', 1)[0].split('\n', 1)[0].split('\n', 1)[0]  # .split('/', 1)[-1].strip()

    return cleaned_text


# Example usage:
input_text = 'Po Robotynės Ukrainos pajėgų laukia kito strateginio miesto išlaisvinimas'
cleaned_text = clean_titles(input_text)
print(cleaned_text)  # Output: "with multiple lines"

# print(clean_titles('„Ignitis“ darbuotojus grąžina atgal į biurą, kiti laisvę pasirinkti vadina pranašumu\r\n\t\t\t\t\t Premium'))
