from pydantic_settings import BaseSettings


class AnimeConfig(BaseSettings):
    MAL_API_KEY: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjlhMGY4ZmVkNTE4YTgwZDZmMzkxOTkyMzU5NjcxOGMxY2ZhYm" \
                       "E3MzM5NDQ3ZDkwNDJjMGU3MzRhM2Q4YWNiODIxMjE2NmUzNzdhN2IyYjkwIn0.eyJhdWQiOiIzZjE3N2ZmNDkyZDk1YTUwN" \
                       "WEyY2RmNWMzYjNiM2EyOSIsImp0aSI6IjlhMGY4ZmVkNTE4YTgwZDZmMzkxOTkyMzU5NjcxOGMxY2ZhYmE3MzM5NDQ3ZD" \
                       "kwNDJjMGU3MzRhM2Q4YWNiODIxMjE2NmUzNzdhN2IyYjkwIiwiaWF0IjoxNzAyOTI0ODU4LCJuYmYiOjE3MDI5MjQ4NTgs" \
                       "ImV4cCI6MTcwNTYwMzI1OCwic3ViIjoiMTQ2MjY0MzkiLCJzY29wZXMiOltdfQ.aUlaA-wMM6dj9giqdElFpQNBFh0nXgh" \
                       "CSlkrtWjkuXpMfaGy9GjohyCd6y0aOWYLoWTn_pjCXBPX_R3TKwdNYjoqz2s4jNXmIQmG432rbXTa7QUPqX42q9Q_RTm-E" \
                       "0fGVKy5Yl77CB2fBT8iOMrWf7iB_y6R9fwysBguwX4zWCRa6rCKK7PjQm3_8G95uzdLlmHJSMRf0nvI6ZZKF4ZHOAXnoqMe" \
                       "dCGXTg5QzrTHSS0-9YSl0QupK_VlC16YvSVob9kT9ovLoo3NtkfiBtpZB-1Yxi2Hjd5MYd0osde-N37hC7oZseF0QwnWRYQ" \
                       "79EuBzCA0DtpIljj2D0hmNQWJ-g"

anime_config = AnimeConfig()
