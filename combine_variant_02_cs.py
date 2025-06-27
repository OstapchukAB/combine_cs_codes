import os
import re

def remove_comments_and_regions(code):
    """Удаляет комментарии, регионы и BOM-символ"""
    # Удаление BOM-символа
    if code.startswith('\ufeff'):
        code = code[1:]
    
    # Удаление комментариев
    pattern = r'("(?:\\"|[^"])*")|/\*.*?\*/|//[^\n]*'
    code = re.sub(pattern, lambda m: m.group(1) if m.group(1) else '', code, flags=re.DOTALL)
    
    # Удаление регионов
    code = re.sub(r'^\s*#\s*region\b.*$|^\s*#\s*endregion\b.*$', '', code, flags=re.MULTILINE)
    return code

def reorganize_code_structure(code):
    """Перестраивает структуру кода: перемещает using внутрь namespace"""
    # Разделение кода на строки
    lines = [line for line in code.splitlines() if line.strip() != '']
    
    # Сбор using-директив и поиск namespace
    using_lines = []
    namespace_index = -1
    namespace_line = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('using ') and stripped.endswith(';'):
            using_lines.append(line)
        elif stripped.startswith('namespace '):
            namespace_index = i
            namespace_line = line.rstrip(';')
            break
    
    # Если namespace не найден, возвращаем исходный код
    if namespace_index == -1:
        return '\n'.join(lines)
    
    # Сбор остального кода
    other_code = lines[namespace_index + 1:]
    
    # Формирование нового кода
    new_code = []
    new_code.append(namespace_line)
    new_code.append('{')
    new_code.extend(using_lines)
    new_code.extend(other_code)
    new_code.append('}')
    
    return '\n'.join(new_code)

def process_csharp_file(file_path):
    """Обрабатывает один C# файл"""
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Очистка кода
    cleaned_code = remove_comments_and_regions(code)
    
    # Реорганизация структуры
    reorganized_code = reorganize_code_structure(cleaned_code)
    
    # Удаление лишних пустых строк
    reorganized_code = re.sub(r'\n\s*\n', '\n\n', reorganized_code)
    return reorganized_code.strip()

def combine_csharp_files(source_dir, output_file):
    """Объединяет все .cs файлы в один"""
    with open(output_file, 'w', encoding='utf-8') as out_f:
        # Добавляем общий заголовок
        out_f.write("// ======== ОБЪЕДИНЕННЫЙ ФАЙЛ C# ========\n\n")
        
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.cs') and file !='combined.cs':
                    file_path = os.path.join(root, file)
                    try:
                        processed_code = process_csharp_file(file_path)
                        
                        # Добавляем разделитель с именем файла
                        out_f.write(f"// ======== ФАЙЛ: {file_path} ========\n\n")
                        out_f.write(processed_code + "\n\n")
                        out_f.write("//" + "=" * 70 + "\n\n")
                    
                    except Exception as e:
                        print(f"Ошибка обработки файла {file_path}: {str(e)}")

if __name__ == "__main__":
    project_root = '.'  # Корневая папка проекта
    output_file = 'combined.cs'  # Итоговый файл
    
    combine_csharp_files(project_root, output_file)
    print(f"Все файлы объединены в {output_file}")