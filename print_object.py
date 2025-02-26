import json
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        # Extract excluded_fields from kwargs if present
        self.excluded_fields = kwargs.pop('excluded_fields', None) or []
        super().__init__(*args, **kwargs)
    
    def default(self, obj):
        # 如果对象是 datetime 类型，转换为 ISO 格式的字符串
        if isinstance(obj, datetime):
            return obj.isoformat()

        # 如果对象是集合类型，转换为列表
        elif isinstance(obj, set):
            return list(obj)

        # 如果对象有 __dict__ 属性，尝试序列化对象的属性
        elif hasattr(obj, '__dict__'):
            # Filter out excluded fields
            return {k: v for k, v in obj.__dict__.items() if k not in self.excluded_fields}

        # 如果对象不可序列化，返回其字符串表示形式
        string = str(obj)
        if len(string) > 100:
            return string[:100] + '...'
        else:
            return string

def print_as_json(obj, excluded_fields=None):
    try:
        json_str = json.dumps(obj, cls=CustomJSONEncoder, indent=4, ensure_ascii=False, excluded_fields=excluded_fields)
        print(json_str)
    except TypeError as e:
        print(f"Error serializing object: {e}")

def save_as_json(obj, filename, excluded_fields=None):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(obj, f, cls=CustomJSONEncoder, indent=4, ensure_ascii=False, excluded_fields=excluded_fields)
    except TypeError as e:
        print(f"Error serializing object: {e}")


if __name__ == "__main__":
    # 示例类
    class ExampleObject:
        def __init__(self, name, value):
            self.name = name
            self.value = value
            self.created_at = datetime.now()

    # 创建对象
    example_obj = ExampleObject("Test", {1, 2, 3})

    # 打印对象为 JSON 格式
    print_as_json(example_obj)
    
    # 打印对象为 JSON 格式，但排除 created_at 字段
    print("\nExcluding 'created_at' field:")
    print_as_json(example_obj, excluded_fields=['created_at'])
    
    # 保存对象为 JSON 文件，但排除 value 字段
    save_as_json(example_obj, "example_without_value.json", excluded_fields=['value'])
