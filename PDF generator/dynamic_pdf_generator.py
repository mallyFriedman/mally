import numpy as np
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_RIGHT
from bidi.algorithm import get_display
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader
import textwrap

# -----Register a font that supports Hebrew characters-----
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

regular_text_style = ParagraphStyle(
    name='RegularTextStyle',
    fontName='Arial',
    fontSize=12,
)

# -----Create a PDF document-----
csv_file = r"C:\Users\USER\Desktop\עבודה\נוכחי\stb_main.csv"
csv_file_2 = r"C:\Users\USER\Desktop\עבודה\נוכחי\stb_dynamic1.csv"
csv_file_3 = r"C:\Users\USER\Desktop\עבודה\נוכחי\stb_dynamic2.csv"
img_url = "https://res.cloudinary.com/benjiazaria/image/upload/v1714663911/image001.png"

df = pd.read_csv(csv_file)
df_2 = pd.read_csv(csv_file_2)
df_3 = pd.read_csv(csv_file_3)

# -----data for the first table-----
data1 = [["יסנניפ סכנב םיתוריש ןתונ", "חוודמה ףוגה גוס"],
            ["מ\"עב ןוינוי .ב.ט.ש", "חוודמה םרוגה לש אלמ םש\n"
                                    "ימושירב ןכדועמש יפכ ,השרומ קסוע וא הרבח -חוודמה לש קיודמו אלמ םש)\n"
                                    "(רצואה דרשמב ןוכסחו חוטיב ןוהה קוש תושר"],
            ["514138288", "חוודמה םרוגה לש ההזמ רפסמ\n"
                          "(השרומ קסוע רפסמ - השרומ קסוע ,.פ.ח - הרבחב)"],
            ["1", "חוודמ ףינס רפסמ\n"
                  "תחוודמה הלועפה העצוב ובש ףינסה **\n"
                  "םייק ויבגלש חוודמ .ה\"לשר םע שארמ םואתב עבקנש ימינפ רפסמ אוה הז רפסמ) \n"
                  "(001 םושרי ,דחא ףינס קר"],
            ["ןויצל ןושאר ,3 רוינס דוד", " ףינסה ןעמ\n"
                                         "תחוודמה הלועפה העצוב ובש ףינסה**"],
            ["20/01/2024", "(DD/MM/YYYY) חווידה תביתכ ךיראת "],
            ["128258", " חוויד רפסמ\n"
                       " םג חוויד רפסמ ותוא לע רוזחל ןיא ,הז חווידל חוודמה לש יכרע דח רפסמ)\n"
                       "תונוש חוויד תונשב חוויד רפסמ ותוא לע רוזחל ןיא ;םינוש םיפינסב"],
            ["055-985-0969", "חוודמה םרוגה לש הלימיסקפו ןופלט"],
            ["ןויצל ןושאר ,3 רוינס דוד", "חוודמה םרוגה ןעמ"],
            [" םיסקמ בוקנפ", "חווידה ךרוע דבוע לש החפשמ םשו יטרפ םש"],
            ["341209443", " חווידה ךרוע לש ז\"ת"],
            ["תויצ ןיצק", "חווידה ךרוע דיקפת"],
            ["055-985-0969", "חווידה ךרוע ןופלט"]]

# -----data for the second table-----
data2 = [["", "יטרפ םש"],
                 ["", "החפשמ םש"],
                 ["", "ראות"],
                 ["", "תוהז רפסמ"],
                 ["", "  תוהזה רפסמ גוס\n"
                      "לש רפסמ /עסמ תדועת /(פ.ח) דיגאת םושיר רפסם / פ.ח / ןוכרד / ז\"ת- : ןוגכ)\n"
                      "(יחרזאה להנמה קיפנהש הדועת"],
                 ["", "תודגאתה תנידמה וא ז\"ת/ןוכרד תנידמ"],
                 ["", " (רוזא בשות/ץוח בשות/בשות) דמעמ"],
                 ["", "הדיל ךיראת"],
                 ["", "ןימ"],
                 ["", "קוסיע"],
                 ["", "דיגאתל רשק\n"
                      "-אמגודל ,הז הדש אלמל שי דיגאת גוסמ העידי אושנ םג ןזוה ליבקמבש לככ)\n"
                      "(טילש לעב כו הלאב אצוי"]]





# -----data for the third table-----

data3 = [["", "דיגאתה לש אלמ םש"],
         ["", "דיגאת םושיר רפסמ"],
         ["", "דיגאתה םושיר ךיראת"],
         ["", "םושירה תנידמ"],
         ["", "םיקסע םוחת רואית"]]

# -----data for the fourth table-----

data4 = [["לעופב ופרוצש םידומע רפסמ", "ךמסמ גוס"],
         ["", "תוריש לבקמ תרהצה ספוט  .1"],
         ["ID, PDF", "יוהיז יכמסמ  .2"],
         ["", "תונמאנ בתכ וא חוכ יופיי  .3"],
         ["", "יטפשמה דיגאתה םושיר ירושיא  .4"],
         ["", "דיגאתב הטילש ילעבו המיתח ישרומ ירושיא  .5"],
         ["", "הכונמ קיש לש (םידדצה ינשמ) מלוצמ קתעה  .6"],
         ["", "תוכז תאחמה קתעה  .7"],
         ["", "(הרבעה רבוש ,SWIFT) הרבעה יכמסמ  .8"],
         ["", "חוקלה תא רכה ספוט  .9"],
         ["", "םיבטומ תמישר  .10"],
         ["", "םיברע תמישר  .11"],
         ["", "המיתח השרומ וא חוכ הפוימ יונימל השקבה ספוט  .12"],
         ["", "תימוא יכמסמ  .13"],
         ["", "האוולה יכמסמ  .14"],
         ["", "האוולהל תוחוטוב  .15"],
         ["", "תפמ ,סיסלאניי'צ - אמגודל) תימינפ רוטינו לוהינ תיכותמ טלפ  .16\n"
              "(הלאב אצויכו םירשק"],
         ["1", "(לסקא ץבוק) העידיה אושנ ידי לע העצובש תולועפ תלבט  .17"],
         ["", "(ךמסמה גוס תא טרפל שי) _______ רחא  .18"]]


# -----style of all the table in the pdf-----
def generate_table_style(first_row_background, middle_row_background, long, font_size):
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), first_row_background),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), font_size),  # Set font size to 8 (adjust as needed)
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]
    if long:
        style.append(('BACKGROUND', (0, 9), (-1, 12), middle_row_background))
    return TableStyle(style)


# -----Styled Table Generator-----
def generate_table(data_table, col_widths, color1, color2, flag, font_size=8):
    table = Table(data_table, colWidths=col_widths)
    table.setStyle(generate_table_style(color1, color2, flag, font_size))
    return table



# -----reverse hebraw words function-----
def reverse_and_correct_hebrew(text):
    return get_display(text)
df['concat_column'] = df['user_id'].astype(str) + df['additional_info'] + df['rule_id'].astype(str)  # Concatenated
# Column Creation


num = 0  # creates the number in the name of pdf

# -----PDF Report Generation with Dynamic Tables and Text Formatting-----
for concat_column in df['concat_column']:

    filtered_df = df[df['concat_column'] == concat_column]
    row_number = filtered_df.index[0]
    df_2['concat_column'] = df_2['user_id'].astype(str) + df_2['additional_info'] + df_2['rule_id'].astype(str)
    df_3['concat_column'] = df_3['user_id'].astype(str) + df_3['additional_info'] + df_3['rule_id'].astype(str)
    filtered_df_2 = df_2[df_2['concat_column'] == concat_column]
    filtered_df_3 = df_3[df_3['concat_column'] == concat_column]

    # df['occupation'] = df['occupation'].fillna('')# no such value...
    filtered_df_2 = filtered_df_2.fillna('')  # replacing nan with ""
    filtered_df_3 = filtered_df_3.fillna('')  # replacing nan with ""

    name = reverse_and_correct_hebrew(filtered_df['first_name'].iloc[0])  # reversing the hebrew words
    last_name = reverse_and_correct_hebrew(filtered_df['last_name'].iloc[0])  # reversing the hebrew words
    pdf_filename = f'combined_tables{num, name, last_name}.pdf'
    num = num + 1
    doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))

    filtered_df_2 = filtered_df_2[filtered_df_2.columns[::-1]]  # Reorder columns in filtered_df_2
    filtered_df_3 = filtered_df_3[filtered_df_3.columns[::-1]]  # Reorder columns in filtered_df_3


    # -----Processing Long Values in DataFrame Columns-----
    def process_long_values(data_f,max_length = 13):
        df_copy = data_f.copy()  # Create a copy of the DataFrame
        for column_name in data_f.columns:
            df_copy[column_name] = df_copy[column_name].apply(
                lambda x: insert_newline(x, max_length) if isinstance(x, str) and len(x) > 10 else x)
        return df_copy


    # -----Function to Insert Newlines in Strings Exceeding Character Limit-----
    def insert_newline(value, max_line_length=13):
        words = value.split()
        lines = [words[0]]
        for word in words[1:]:
            if len(lines[-1]) + len(word) + 1 <= max_line_length:
                lines[-1] += ' ' + word
            else:
                lines.append(word)
        return '\n'.join(lines)


    filtered_df_2_processed = process_long_values(filtered_df_2, 20)  # Applying the function to the filtered DataFrames
    filtered_df_3_processed = process_long_values(filtered_df_3)  # Applying the function to the filtered DataFrames

    # -----pulls from csv details for the second table-----
    rows_to_fill = [(0, 'first_name'), (1, 'last_name'), (3, 'sender_id_number'),
                    (4, 'sender_id_type'), (5, 'sender_id_issue_by_country'),
                    (7, 'birth_date'), (8, 'sender_country'),  # suppose to be 'sender_gender'
                    # (9, 'occupation')
                    ]

    for row, column_name in rows_to_fill:
        data2[row][0] = filtered_df.loc[row_number, column_name]

    sender_city_value = filtered_df['sender_city'].iloc[0]  # pulls from csv data for the pdf
    sender_address_value = filtered_df['sender_address'].iloc[0]  # pulls from csv data for the pdf
    sender_zip_code_value = filtered_df['sender_zip_code'].iloc[0]  # pulls from csv data for the pdf
    tamtzit_value = reverse_and_correct_hebrew(filtered_df['tamtzit'].iloc[0])  # pulls from csv data for the pdf

    row_values = [
        reverse_and_correct_hebrew(filtered_df[col].iloc[0]) if isinstance(filtered_df[col].iloc[0], str) else ''
        for col in ['row_1', 'row_2', 'row_3', 'row_4', 'row_5', 'row_6', 'row_7']
    ]

    row_1_value, row_2_value, row_3_value, row_4_value, row_5_value, row_6_value, row_7_value = row_values

    # -----Creating Dynamic Table Data with Custom Column Titles-----
    dynamic_table_data = []
    column_titles = [col for col in filtered_df_2_processed.columns
                     if col not in ['user_id', 'concat_column', 'rule_id', 'additional_info', 'internal_sorting',
                                    'internal_ranking']]

    if not filtered_df_2_processed.empty:
        filtered_df_2_processed['relation'] = filtered_df_2_processed['relation'].apply(reverse_and_correct_hebrew)

    for _, row in filtered_df_2_processed.iterrows():
        dynamic_table_data.append([row[column] for column in column_titles])

        new_column_titles = {
            'full_name': "דיגאת / החפשמ םשו יטרפ םש",
            'id_number': "םושיר / ןוכרד / תוהז רפסמ",
            'relation': "העידיה אשונל רשק",
            'address_type': "תבותכ גוס",
            'address_name': "תבותכ לעב םש",
            'country': "זוחמ -רוזא / הנידמ",
            'city': "בושי םוקמ",
            'address': "רפסמו בוחר",
            'po_box': " .ד.ת",
            'notes': "תופסונ תורעה",
        }

    # Update column titles
    column_titles = [new_column_titles.get(column, column) for column in column_titles]
    # Insert column titles at the beginning of dynamic_table_data
    dynamic_table_data.insert(0, column_titles)
    # Define column widths
    dynamic_table_col_widths = [60, 40, 90, 90, 73, 61, 51, 95, 95, 115, 90]
    # Construct the table
    table_dynamic_1 = Table(dynamic_table_data, colWidths=dynamic_table_col_widths)

    # -----Creating Dynamic Table Data with Custom Column Titles-----
    dynamic_table_data_2 = []
    column_titles_2 = [col for col in filtered_df_3_processed.columns
                       if col not in ['concat_column', 'user_id', 'rule_id', 'additional_info']]

    for _, row in filtered_df_3_processed.iterrows():
        dynamic_table_data_2.append([row[column] for column in column_titles_2])
    # Add mappings for other columns if needed
    new_column_titles_2 = {
        'id_type': "ההזמ הדועת גוס",
        'id_county': "חוקלה תדועת תנידמ",
        'id': "ההזמ הדועת רפסמ",
        'recipient_country': "דעי תנידמ",
        'transaction_type': "ןוויכ",
        'currency': "עבטמה םש",
        'amount': "עבטמב םוכס",
        'amount_ils': "םילקשב םוכס",
        'reciever': "לבקמה םש",
        'city': "ןכוס ריע",
        'street': "ןכוס תובתכ",
        'registration_number': "ןכוס פ.ח",
        'name': "ןכוסה םש",
        'transaction_id': "הקסעה רפסמ",
        'action_date': "הלועפ ךיראת",
    }

    # Update column titles
    column_titles_2 = [new_column_titles_2.get(column, column) for column in column_titles_2]
    # Insert column titles at the beginning of dynamic_table_data
    dynamic_table_data_2.insert(0, column_titles_2)
    # Define column widths
    dynamic_table_2_col_widths = [47, 57, 59, 44, 59, 59, 59, 44, 45, 40, 44, 41, 59, 65, 54]
    # Construct the table
    table_dynamic_2 = Table(dynamic_table_data_2, colWidths=dynamic_table_2_col_widths)

# -----Styling Tables with Various Data Sources-----
    font_size_1 = 8.5
    font_size_2 = 7
    table1 = generate_table(data1, [240, 260], colors.lightgrey, colors.grey, True)
    table2 = generate_table(data2, [240, 260], colors.white, colors.white, False)
    table3 = generate_table(data3, [240, 260], colors.white, colors.white, False)
    table4 = generate_table(data4, [240, 260], colors.lightgrey, colors.white, False)
    table_dynamic_1.setStyle(generate_table_style(colors.lightgrey, colors.white, False, font_size_1))
    table_dynamic_2.setStyle(generate_table_style(colors.lightgrey, colors.white, False, font_size_2))

# -----function to replace nan with: ""
    def clean_value(value):
        if value == 'nan':
            return ""
        return str(value)



    # -----the text in the pdf-----
    caption1 = "וצל (ב)11 ףיעס יפל הליגר יתלב הלועפ לע חווידל תינבת .1"
    caption2 = "<u>חוודמה יטרפ</u> .1.2"
    # Caption for the second table
    caption3 = "<u>העידיה אושנ</u> .1.3"
    caption4 = "דיחי 2.3.1"
    caption5 = "דיגאת 2.3.2"
    caption6 = ":העידיה אושנ ןעמ"
    sender_zip_code_value = "{:.0f}".format(sender_zip_code_value)
    sender_zip_code = clean_value(sender_zip_code_value)
    text1 = f"{sender_city_value} / {sender_address_value} / {sender_zip_code}"
    caption7 = "<u>העידיה תיצמת</u> .2.4 "
    text2 = f"{tamtzit_value}"
    caption8 = "<u>(םבלשל רחב חוודמה םאו םימייק םא אשונב אציש ידועיי רזוח יפל) חתפמ יוטיב</u> .2.5"
    # New lines with just underlines
    empty_line1 = "<u>____________________________________________________________________________</u>"
    empty_line2 = "<u>____________________________________________________________________________</u>"
    empty_line3 = "<u>____________________________________________________________________________</u>"
    caption9 = "<u>:העידיה ןכות</u> .2.6"
    text3 = f"{row_1_value}"
    text4 = f"{row_2_value}"
    text5 = f"{row_3_value}"
    text6 = f"{row_4_value}"
    text7 = f"{row_5_value}"
    text8 = f"{row_6_value}"
    text9 = f"{row_7_value}"
    caption10 = "<u>העידיה ןכותב םיברועמ םימרוג</u> .2.7"
    caption11 = "<u>חווידה תלוכת טוריפ</u> .2.8"
    caption12 = "<u>055-985-0969</u> :ןופלט <u>תויצ ןיצק</u> :דיקפת <u>םיסקמ בוקנפ</u> :(חוידה ךרוע) החפשמו םש "
    caption13 = "<u>20/01/2024</u> :העשו ךיראת <u> m.pankov@stbunion.com </u> :ינורטקלא ראוד <u>055-985-0969</u> :הילמיסקפ "
    caption14 = ":המיתח"


    # -----Generate Paragraph objects for text4, text5, text6, and text7 with the desired font size-----

    base_style = regular_text_style.clone('BaseStyle')
    # Set the desired properties for all Paragraphs
    base_style.fontSize = 10
    base_style.alignment = 2

    # Create Paragraph objects with the base style
    text3_paragraph = Paragraph(text3, style=base_style)
    text4_paragraph = Paragraph(text4, style=base_style)
    text5_paragraph = Paragraph(text5, style=base_style)
    text6_paragraph = Paragraph(text6, style=base_style)
    text7_paragraph = Paragraph(text7, style=base_style)
    text8_paragraph = Paragraph(text8, style=base_style)
    text9_paragraph = Paragraph(text9, style=base_style)

    paragraph_mapping = {
        'text3': text3_paragraph,
        'text4': text4_paragraph,
        'text5': text5_paragraph,
        'text6': text6_paragraph,
        'text7': text7_paragraph,
        'text8': text8_paragraph,
        'text9': text9_paragraph
    }

    captions = {
        'caption1': caption1, 'caption2': caption2, 'caption3': caption3,
        'caption4': caption4, 'caption5': caption5, 'caption6': caption6,
        'caption7': caption7, 'caption8': caption8, 'empty_line1': empty_line1,
        'empty_line2': empty_line2, 'empty_line3': empty_line3, 'caption9': caption9,
        'caption10': caption10, 'caption11': caption11, 'caption12': caption12,
        'caption13': caption13, 'caption14': caption14,
        'text1': text1, 'text2': text2,
    }

    # -----style for the pdf-----
    caption_paragraphs = {
        key: Paragraph(value, style=ParagraphStyle(name='CaptionStyle', fontName='Arial', alignment=TA_RIGHT)) for
        key, value in captions.items()}

    # -----Build the PDF-----

    elements = []

    order = ['caption1', 'caption2', 'table1', 'caption3',
             'caption4', 'table2', 'caption5', 'table3',
             'caption6', 'text1', 'caption7', 'text2', 'caption8',
             'empty_line1', 'empty_line2', 'empty_line3', 'caption9',
             'text3', 'text4', 'text5', 'text6', 'text7', 'text8', 'text9', 'caption10',
             'dynamic_table', 'caption11', 'table4',
             'caption12', 'caption13', 'caption14', 'img', 'dynamic_table_2']
    for item in order:

        if item in caption_paragraphs:
            # and item not in ['text3', 'text4', 'text5', 'text6', 'text7']:
            elements.append(caption_paragraphs[item])
            elements.append(Spacer(1, 12))
        if item in paragraph_mapping:
            elements.append(paragraph_mapping[item])
            elements.append(Spacer(1, 12))
        elif item == 'table1':
            elements.append(table1)
            elements.append(Spacer(1, 12))
        elif item == 'table2':
            elements.append(table2)
            elements.append(Spacer(1, 12))
        elif item == 'table3':
            elements.append(table3)
            elements.append(Spacer(1, 12))
        elif item == 'table4':
            elements.append(table4)
            elements.append(Spacer(1, 12))
        elif item == 'dynamic_table':
            elements.append(table_dynamic_1)
            elements.append(Spacer(1, 12))
        elif item == 'dynamic_table_2':
            elements.append(table_dynamic_2)
            elements.append(Spacer(1, 12))
        if item == 'img':
            elements.append(Image(img_url, width=50, height=50))  # Adjust width and height as needed
            elements.append(Spacer(1, 12))  # Add spacer for formatting

    doc.build(elements)

    print(f"PDF created successfully: {pdf_filename}")
    #doc_letter = SimpleDocTemplate(f'combined_tables_letter{num, name, last_name}.pdf', pagesize=letter)
    #doc_letter.build(elements)

    # Generate PDF with landscape size page
    #doc_landscape = SimpleDocTemplate(f'combined_tables_landscape{num, name, last_name}.pdf', pagesize=landscape(letter))
    #doc_landscape.build(elements_landscape)