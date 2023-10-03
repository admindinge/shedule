#!/bin/bash

# считываем код школы из файла
school_code=$(cat "/opt/school")

# Скачиваем файл с расписанием с GitHub
github_file_url="https://raw.githubusercontent.com/admindinge/shedule/main/${school_code}"
temp_file_path="./temp"
curl -sSL "$github_file_url" -o "$temp_file_path"

# Проверяем изменения в файле
new_hash=$(sha256sum "$temp_file_path" | awk '{print $1}')
if [ -f "previous" ]; then
    previous_hash=$(cat "previous")
    if [ "$new_hash" == "$previous_hash" ]; then
        echo "ᲤᲐᲘᲚᲘ ᲐᲠ ᲨᲔᲪᲕᲚᲘᲚᲐ"
        exit 0
    fi
fi

# Сохраняем текущий crontab в файл
crontab -l > "current_crontab.txt"

# Обновляем crontab из файла temp_file_path
crontab "$temp_file_path"



# Обновляем хеш в файле
echo "$new_hash" > "previous"

echo "ᲤᲐᲘᲚᲘ ᲨᲔᲪᲕᲚᲘᲚᲘ, ᲒᲐᲜᲐᲮᲚᲔᲑᲣᲚᲘᲐ ᲒᲐᲜᲠᲘᲒᲘᲪ ᲓᲐ ᲮᲔᲨᲘᲪ."


# Вызываем filetool.sh для сохранения изменений, включая crontab
filetool.sh -b
