import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not configured")


    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cde_lab.db")
    #1. __file__: đường dẫn đến file config.py.
    #2. os.path.abspath(__file__): lấy đường dẫn tuyệt đối của file.
    #3. os.path.dirname(...): lấy thư mục chứa config.py.
    #4. os.path.join(..., "cde_lab.db"): ghép thư mục đó với tên file database.

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    # 1. DATABASE_PATH là địa chỉ nhà.
    # 2. SQLALCHEMY_DATABASE_URI là thông tin kết nối để SQLAlchemy tìm đến địa chỉ đó.

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-SQLAlchemy có cơ chế theo dõi các thay đổi của đối tượng để phát ra tín hiệu. Đặt False sẽ tắt cơ chế theo dõi bổ sung đó, giúp tránh phần chi phí tài nguyên không cần thiết.

    # ENV = os.getenv("FLASK_ENV", "development")
    #1. ENV: biến cấu hình môi trường của dự án.
    #2. os.getenv("FLASK_ENV", "development"): đọc biến môi trường FLASK_ENV; nếu chưa có thì dùng giá trị mặc định "development".
    
    