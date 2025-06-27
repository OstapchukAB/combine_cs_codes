import os
import re

def clean_csharp_code(code):
    """Очищает код C# от комментариев, регионов и BOM-символа"""
    # Удаление BOM-символа (U+FEFF)
    if code.startswith('\ufeff'):
        code = code[1:]
    
    # Удаление однострочных и многострочных комментариев
    pattern = r'("(?:\\"|[^"])*")|/\*.*?\*/|//[^\n]*'
    code = re.sub(pattern, lambda m: m.group(1) if m.group(1) else '', code, flags=re.DOTALL)
    
    # Удаление #region и #endregion
    code = re.sub(r'^\s*#\s*region\b.*?$|^\s*#\s*endregion\b.*?$', '', code, flags=re.MULTILINE)
    
    # Удаление лишних пустых строк
    code = re.sub(r'\n\s*\n', '\n\n', code)
    
    return code.strip()

def combine_csharp_files(source_dir, output_file):
    """Объединяет все .cs файлы в один"""
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.cs'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                        
                        cleaned = clean_csharp_code(content)
                        
                        # Добавляем разделитель с именем файла
                        outfile.write(f"// ----- {file_path} -----\n\n")
                        outfile.write(cleaned + "\n\n")
                        outfile.write("//" + "/" * 70 + "\n\n")
                    
                    except Exception as e:
                        print(f"Ошибка обработки файла {file_path}: {str(e)}")

if __name__ == "__main__":
    source_directory = '.'  # Стартовая директория
    output_filename = 'combined.cs'  # Итоговый файл
    
    combine_csharp_files(source_directory, output_filename)
    print(f"Все файлы объединены в {output_filename}")