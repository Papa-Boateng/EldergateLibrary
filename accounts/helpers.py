
#Styling Functions
def get_book_type_from_price(dashboard_type, price):
    if price == 0:
        class_sheet = "text-xs font-semibold bg-dark-success text-green-500 px-2 py-1 rounded-full self-start"
        text = "Free"
        book_type = "Free"
    else:
        if dashboard_type == 'reader':
            class_sheet = "text-xs font-semibold bg-dark-success text-blue-500 px-2 py-1 rounded-full self-start"
        else:   
            class_sheet = "text-xs font-semibold bg-primary text-white px-2 py-1 rounded-full self-start"
        text = f"${price}"
        book_type = "Paid"
    return class_sheet, text, book_type

def user_category_class(category):
    if category == "Fiction":
        class_sheet = "text-xs font-semibold text-blue-500 bg-blue-500/10 py-1 px-2 rounded-full"
    elif category == "Mystery":
        class_sheet = "text-xs font-semibold text-yellow-500 bg-yellow-500/10 py-1 px-2 rounded-full"
    elif category == "Philosophy":
        class_sheet = "text-xs font-semibold text-green-500 bg-green-500/10 py-1 px-2 rounded-full"
    elif category == "History":
        class_sheet = "text-xs font-semibold text-purple-500 bg-purple-500/10 py-1 px-2 rounded-full"
    elif category == "Biography":
        class_sheet = "text-xs font-semibold text-pink-500 bg-pink-500/10 py-1 px-2 rounded-full"
    else:
        class_sheet = "text-xs font-semibold text-red-500 bg-red-500/10 py-1 px-2 rounded-full"
    
    return class_sheet


def admin_book_management_bt(price):
    if price == 0:
        class_sheet = "px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 dark:bg-green-800/30 text-green-800 dark:text-green-300"
        text = "Free"
    else:
        class_sheet = "px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 dark:bg-blue-800/30 text-blue-800 dark:text-blue-300"
        text = "Paid"
    return class_sheet, text

def admin_book_management_category(category):
    if category == "Fiction":
        class_sheet = "text-xs font-semibold text-blue-500 bg-blue-500/10 py-2 px-6 rounded-full"
    elif category == "Mystery":
        class_sheet = "text-xs font-semibold text-yellow-500 bg-yellow-500/10 py-2 px-6 rounded-full"
    elif category == "Philosophy":
        class_sheet = "text-xs font-semibold text-green-500 bg-green-500/10 py-2 px-6 rounded-full"
    elif category == "History":
        class_sheet = "text-xs font-semibold text-purple-500 bg-purple-500/10 py-2 px-6 rounded-full"
    elif category == "Biography":
        class_sheet = "text-xs font-semibold text-pink-500 bg-pink-500/10 py-2 px-6 rounded-full"
    else:
        class_sheet = "text-xs font-semibold text-red-500 bg-red-500/10 py-2 px-6 rounded-full"
    
    return class_sheet


##Librarian Book Management Functions##
def librarian_book_management_category(category):
    if category == "Fiction":
        class_sheet = "px-6 py-4 whitespace-nowrap text-sm text-blue-600 dark:text-secondary-text"
    elif category == "Mystery":
        class_sheet = "px-6 py-4 whitespace-nowrap text-sm text-yellow-600 dark:text-secondary-text"
    elif category == "Philosophy":
        class_sheet = "px-6 py-4 whitespace-nowrap text-sm text-green-600 dark:text-secondary-text"
    elif category == "History":
        class_sheet = "px-6 py-4 whitespace-nowrap text-sm text-purple-600 dark:text-secondary-text"
    elif category == "Biography":
        class_sheet = "px-6 py-4 whitespace-nowrap text-sm text-pink-600 dark:text-secondary-text"
    else:
        class_sheet = "px-6 py-4 whitespace-nowrap text-sm text-red-600 dark:text-secondary-text"
    
    return class_sheet

def isbn_formatter(isbn_string):
    """
    Formats a 13-digit ISBN string into a standard hyphenated format.
    Example: "9780525536291" -> "978-0-525-53629-1"
    """
    if not isinstance(isbn_string, str) or not isbn_string.isdigit() or len(isbn_string) != 13:
        return isbn_string # Return original string if not a valid 13-digit string

    parts = [
        isbn_string[0:3],
        isbn_string[3:4],
        isbn_string[4:7],
        isbn_string[7:12],
        isbn_string[12:13]
    ]
    return "-".join(parts)
