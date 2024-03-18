import csv
from PIL import Image

braille_characters = list()
with open('braille.csv') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        braille_characters.append(
            {
                'character': row[4],
                'dots_info': row[3],
            }
        )
    braille_characters = braille_characters[1:]

for item in braille_characters:
    info = item['dots_info']
    array = [False] * 6
    for character in info:
        if character.isnumeric():
            array[int(character) - 1] = True
    item.pop('dots_info')
    item['array'] = array

image = Image.open('input3.png').convert('RGB')
pixels = image.load()

rows = image.size[1]
if rows % 3 != 0:
    rows += 3 - (rows % 3)

columns = image.size[0]
if columns % 2 != 0:
    columns += 2 - (columns % 2)

image_average = 0
for row in range(image.size[1]):
    for column in range(image.size[0]):
        pixel_color = pixels[column, row]
        pixel_color_average = int((pixel_color[0] + pixel_color[1] + pixel_color[2]) / 3)
        image_average += pixel_color_average
image_average /= (image.size[0] * image.size[1])

with open('output.html', 'w') as html_file:
    for threshold in range(255, -1, -1):
        html_file.write(
            '<html><meta charset="UTF-8">' +
            '<body style="font-family:monospace;color:rgb(255,255,255);background-color:rgb(20,20,20);">',
        )

        matrix = [[False for i in range(columns)] for j in range(rows)]
        for row in range(image.size[1]):
            for column in range(image.size[0]):
                pixel_color = pixels[column, row]
                pixel_color_average = int((pixel_color[0] + pixel_color[1] + pixel_color[2]) / 3)
                if pixel_color_average >= threshold:
                    matrix[row][column] = True

        for row_character_index in range(int(len(matrix) / 3)):
            for column_character_index in range(int(len(matrix[0]) / 2)):
                p1 = matrix[row_character_index * 3 + 0][column_character_index * 2 + 0]
                p2 = matrix[row_character_index * 3 + 1][column_character_index * 2 + 0]
                p3 = matrix[row_character_index * 3 + 2][column_character_index * 2 + 0]
                p4 = matrix[row_character_index * 3 + 0][column_character_index * 2 + 1]
                p5 = matrix[row_character_index * 3 + 1][column_character_index * 2 + 1]
                p6 = matrix[row_character_index * 3 + 2][column_character_index * 2 + 1]
                array = [p1, p2, p3, p4, p5, p6]
                for item in braille_characters:
                    if item['array'] == array:
                        html_file.write(item['character'])
            html_file.write('<br>')
        html_file.write('<br><br>')
    html_file.write('</body></html>')
