from app.utils import create_jwt_token

token = create_jwt_token("test_user01")
print(f"你的JWT token:\n{token}")
