import requests
import re
import itertools
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

# Добавить больше слов
base_keywords = [
    "наркотики", "наркотик", "нарко", "наркошоп", "дурь", "дурьмо", "герыч", "кокс", "спайс", "марихуана", 
    "травка", "гашиш", "крокодил", "синька", "дизоморфин", "экстази", "шишки", "грибы", "план", "химка", 
    "фен", "мет", "амфетамин", "лсд", "гидропоника", "экста", "метамфетамин", "барбитураты", "опиаты"
]

# Добавить больше 
replacements = {
    'а': ['а', '@', 'a', '4', 'а', 'д', 'α', 'ä', 'ą', 'λ', 'æ', 'ã', 'å', 'ä', 'α', 'ą', 'å', 'à', 'â', 'á'],
    'о': ['о', '0', 'o', 'ø', 'ö', 'θ', 'ó', 'ò', 'õ', 'ô', 'ō', 'ο', 'σ', 'ɵ', 'օ', 'ȯ', 'º', '¤', 'õ', '⊕'],
    'и': ['и', '1', 'i', '!', '|', 'ï', 'í', 'ì', 'î', 'į', 'į', 'ī', '¡', 'ι', '¡', 'ỉ', 'ǐ', 'ĭ', 'Ї', 'ℹ'],
    'к': ['к', 'k', 'c', 'к', 'ĸ', 'κ', 'қ', 'к', 'ƙ', 'ķ', 'K', 'к', 'ĸ', 'κ', 'K', 'Қ', 'ҝ', 'Ҝ', 'Қ', 'Ҡ'],
    'е': ['е', 'e', '3', 'é', 'è', 'ê', 'ë', 'ē', 'ė', 'ε', 'ə', 'ě', 'ӗ', 'ē', 'é', 'ё', 'ę', 'ê', 'ě', 'ȅ'],
    'р': ['р', 'p', 'r', 'ρ', 'р', 'ɹ', 'ř', 'ṝ', 'ŕ', 'ɽ', 'ŗ', 'ҏ', 'ҋ', 'ṛ', 'р', 'ŗ', 'ř', 'г', 'г', 'ր'],
    'т': ['т', 't', '7', 'τ', 'т', 'ť', 'ţ', 'ṫ', 'ŧ', 'т', 'ţ', 'ť', 'ŧ', 'ť', 'ṯ', 'ṱ', 'т', 'ŧ', 'ṱ', 'Ҭ'],
    'с': ['с', 'c', '$', 'ç', '¢', 'с', 'ĉ', 'č', 'ċ', 'ç', 'ç', 'с', 'ĉ', 'ç', 'ċ', 'ć', '¢', 'с', 'ς', 'ҫ'],
    'н': ['н', 'h', 'ɦ', 'њ', 'н', 'ҥ', 'Ң', 'Ҥ', 'ɧ', 'н', 'ħ', 'н', 'Һ', 'Һ', 'ņ', 'н', 'н', 'њ', 'н', 'ң'],
    'м': ['м', 'm', 'ṃ', 'м', 'ṁ', 'ṃ', 'м', 'ӎ', 'м', 'ṁ', 'м', 'ḿ', 'ṁ', 'м', 'ḿ', 'ṁ', 'м', 'м', 'м', 'м'],
    'г': ['г', 'g', 'ğ', 'г', 'ĝ', 'ġ', 'ǵ', 'ĝ', 'ġ', 'ģ', 'ğ', 'г', 'ǧ', 'ģ', 'ǵ', 'ğ', 'г', 'ĝ', 'Ҕ', 'ҕ'],
    'ш': ['ш', 'w', 'щ', 'ш', 'ŝ', 'ш', 'щ', 'š', 'ș', 'ш', 'ŝ', 'š', 'ș', 'щ', 'ш', 'š', 'ш', 'ш', 'щ', 'ш']
}

# Добавить больше 
delimiters = ['', '.', '-', '_', ' ', '|']

def generate_mutations(keyword):
    mutations = set()
    
    char_variants = [replacements.get(char, [char]) for char in keyword]
    for mutation in itertools.product(*char_variants):
        mutations.add(''.join(mutation))
    
    for mutation in list(mutations):
        for delimiter in delimiters:
            spaced_word = delimiter.join(mutation)
            mutations.add(spaced_word)
    
    for word in list(mutations):
        for i in range(1, 5):
            mutations.add(f"{word}{i}")
    
    return list(mutations)

def generate_keyword_list():
    all_variants = set()
    for keyword in base_keywords:
        all_variants.update(generate_mutations(keyword))
    return all_variants

def check_site(url, keyword_list):
    result = {
        'url': url,
        'redirected': False,
        'found_keywords': [],
        'status': ''
    }
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.history:
            result['redirected'] = True
            print(f"[ПРЕДУПРЕЖДЕНИЕ] Перенаправление произошло: {url}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()
        
        for keyword in keyword_list:
            if re.search(rf'\b{keyword}\b', text):
                print(f"[НАЙДЕНО] Запрещенное слово '{keyword}' найдено на сайте: {url}")
                result['found_keywords'].append(keyword)
        
        result['status'] = "Проверено"
    except requests.RequestException as e:
        print(f"[ОШИБКА] Не удалось получить доступ к сайту: {url}. Ошибка: {str(e)}")
        result['status'] = "Ошибка"
    
    return result


def check_sites_from_file(file_path, keyword_list):
    with open(file_path, 'r') as file:
        sites = file.readlines()
    
    results = []
    
    for site in tqdm(sites, desc="Проверка сайтов"):
        site = site.strip()
        if site:
            result = check_site(site, keyword_list)
            results.append(result)
    
    with open('results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)
    
    print(f"\n[ОТЧЕТ] Результаты сохранены в 'results.json'")

def main():
    parser = argparse.ArgumentParser(description='Парсинг сайтов и поиск запрещенных слов.')
    parser.add_argument('--generate', action='store_true', help='Генерация списка запрещенных слов.')
    parser.add_argument('--site', type=str, help='URL сайта для проверки.')
    parser.add_argument('--file', type=str, help='Файл с сайтами для проверки.')
    
    args = parser.parse_args()
    
    if args.generate:
        keywords = generate_keyword_list()
        with open('keywords.txt', 'w') as f:
            for keyword in keywords:
                f.write(f"{keyword}\n")
        print(f"Список запрещенных слов успешно сгенерирован и сохранен в 'keywords.txt'.")
    else:
        with open('keywords.txt', 'r') as f:
            keywords = set(line.strip() for line in f.readlines())
        
        if args.site:
            result = check_site(args.site, keywords)
            with open('results.json', 'w') as json_file:
                json.dump([result], json_file, indent=4, ensure_ascii=False)
            print(f"\n[ОТЧЕТ] Результаты для сайта '{args.site}' сохранены в 'results.json'")
        
        if args.file:
            check_sites_from_file(args.file, keywords)

if __name__ == "__main__":
    main()
