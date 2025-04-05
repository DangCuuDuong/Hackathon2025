import re

def clean_ingredient_name(raw_input: str) -> str:
    """
    Chuẩn hóa tên nguyên liệu:
    - Lowercase
    - Xóa khoảng trắng 2 đầu
    - Xóa ký tự đặc biệt
    - Chuyển số nhiều cơ bản về số ít (tomatoes -> tomato)
    """
    # Bỏ khoảng trắng và lowercase
    name = raw_input.strip().lower()

    # Loại bỏ ký tự đặc biệt, giữ lại a-z và khoảng trắng
    name = re.sub(r"[^a-z\s]", "", name)

    # Nếu có nhiều từ, chỉ giữ từ đầu tiên (hoặc tùy chọn)
    name = name.split()[0] if name else ""

    # Xử lý số nhiều cơ bản
    if name.endswith("ies"):
        name = name[:-3] + "y"  # berries → berry
    elif name.endswith("oes"):
        name = name[:-2]       # potatoes → potato
    elif name.endswith("es"):
        name = name[:-2]       # tomatoes → tomato
    elif name.endswith("s") and len(name) > 3:
        name = name[:-1]       # eggs → egg

    return name
