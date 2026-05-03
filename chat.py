# 目标
#设计并实现一个基础聊天机器人，包含以下功能：
#- 用户输入处理
#- API调用与响应获取
#- 简单的错误处理机制
#- 基本的对话历史管理

import json
from zhipuai import ZhipuAI

api_key = ""
client = ZhipuAI(api_key="")

class ChatAssistant():
    def __init__(self,user_name,api_key,history_file=None,max_history=10):
        self.client = ZhipuAI(api_key=api_key)
        self.user_name = user_name if user_name else "default_user"
        self.history_file = history_file if history_file else f"{self.user_name}_history.json"
        self.max_history = max_history # 最大历史记录条数
        self.conservation_history = [] # 对话历史
        self.display_history = [] # 显示给用户的历史
        self.load_history()

    def load_history(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.display_history = data.get("display_history", [])
                self.conservation_history = data.get("conservation_history", [])
                print(f"已加载 {len(self.display_history)} 条历史对话")
        except FileNotFoundError:
            print("没有找到历史记录文件，开始新的对话")
            self.display_history = []
            self.conservation_history = []
        except json.JSONDecodeError:
            print("历史记录文件格式错误，开始新的对话")
            self.display_history = []
            self.conservation_history = []
        
    def save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                data = {
                    "display_history": self.display_history,
                    "conservation_history": self.conservation_history
                }
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"已保存 {len(self.display_history)} 条历史对话到 {self.history_file}")
        except Exception as e:
            print(f"保存历史记录时出错: {e}")
        

    def add_to_history(self, user_input, response):
        self.display_history.append({""
        "user": user_input, 
        "assistant": response, 
        "timestamp": self.get_timestamp()})
        self.conservation_history.append({"role": "user", "content": user_input})
        self.conservation_history.append({"role": "assistant", "content": response})

        if len(self.conservation_history) > self.max_history *2: # *2 是因为每次对话包含用户和助手两条记录
            self.conservation_history = self.conservation_history[-self.max_history *2:]
        if len(self.display_history) > self.max_history:
            self.display_history = self.display_history[-self.max_history:]

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_response(self, user_input):
        try:
            messages = [] # 构建包含历史对话的消息列表

            messages.append({"role": "system", "content": "你是一个有帮助的AI助手。请根据对话历史提供连贯，清晰的回复"}) # 系统提示

            messages.extend(self.conservation_history) # 添加对话历史

            messages.append({"role": "user", "content": user_input}) # 添加当前用户输入

            response = self.client.chat.completions.create(
                model="glm-4-flash-250414",
                messages=messages,
                max_tokens=1024, # 控制回复的长度
                temperature=0.7, # 控制回复的随机性
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"调用API时出错: {e}")
            return "抱歉，处理您的请求时出现错误。"

    def show_history(self):
        if not self.display_history:
            print("没有历史对话记录。")
            return
        print("\n历史对话记录：")
        for i, entry in enumerate(self.display_history[-5], 1): # 只显示最近5条记录
            print(f"\n{i}. {entry.get('timestamp', 'Unknown Time')}")
            print(f"用户: {entry['user']}")
            print(f"助手: {entry['assistant']}")
        print("=" * 20)
    
    def clear_history(self):
        self.display_history = []
        self.conservation_history = []
        print("对话历史已清除。")

    def start_chat(self):
        print(f"你好，{self.user_name}！我是一个智能聊天机器人，你可以随时找我聊天！")
        print("我支持多轮对话，能够记住我们之前的谈话内容。")
        print("""
可用命令：
- 直接输入：开始对话
- 'quit'：退出对话
- 'history'：查看对话历史
- 'clear'：清除对话历史
- 'help'：显示帮助信息
              """)
        
        if self.display_history:
            print(f"检测到{len(self.display_history)} 条历史对话, 继续上次的对话吧！")

        while True:
            user_input = input(f"/n{self.user_name}: ") .strip()
        
            if not user_input:
               print("输入不能为空，请重新输入。")
               continue
           
            if user_input.lower() == "quit":
               print("感谢使用，再见！")
               break
            elif user_input.lower() == "history":
               self.show_history()
               continue
            elif user_input.lower() == "clear":
                self.clear_history()
                continue
            elif user_input.lower() == "help":
                print("""
可用命令：
- 直接输入：开始对话
- 'quit'：退出对话
- 'history'：查看对话历史
- 'clear'：清除对话历史
- 'help'：显示帮助信息
                 """)
                continue
           
            print("AI 正在思考...")
            response = self.get_response(user_input)    
            print(f"AI 助手: {response}")


            self.add_to_history(user_input, response)

            if "抱歉，处理您的请求时出现错误" in response:
                retry = input("是否重试？(y/n): ").lower()
                if retry != 'y':    
                    break
        print("聊天结束，期待下次再见！")
        self.save_history()

def main(user_name=input("请输入您的姓名: (回车可进入游客模式)"),history_file=None):
    assistant = ChatAssistant(
        user_name=user_name,
        api_key=api_key,
        history_file=history_file)
    assistant.start_chat()


if __name__ == "__main__":
    main() 