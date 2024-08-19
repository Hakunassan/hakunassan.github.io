import os
import sys
import subprocess
from datetime import datetime


def create_post(title):
    today = datetime.today()
    formatted_date = today.strftime("%Y%m%d")
    file_name = f"content/posts/{today.year}/{formatted_date}_{title}.md"
    image_dir = f"static/images/posts/{today.year}/{formatted_date}_{title}"

    # 创建 Markdown 文件
    subprocess.run(["hugo", "new", file_name])

    # 创建图片文件夹
    os.makedirs(image_dir, exist_ok=True)  # exist_ok=True 确保文件夹不存在时才创建

    print(f"Post created successfully: {file_name}")
    print(f"Image directory created: {image_dir}")
    return file_name


def replace_title_in_post(file_path, title):
  """
  Replaces the title in a post file using pure Python.

  Args:
      file_path (str): Path to the post file.
      title (str): New title to replace the existing one.
  """
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines[2] = 'title: ' + title + '\n'  # 注意：这里需要加上换行符
        lines[3] = 'slug: ' + title + '\n'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Title replaced successfully in {file_path}")
  except FileNotFoundError:
    print(f"Error: File not found: {file_path}") 
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
    title = sys.argv[1]
    file_path = create_post(title)
    replace_title_in_post(file_path, title)