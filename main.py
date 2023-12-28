from rich.console import Console
import datetime
from params import *
from rag import query

console = Console()

def timestamp():
    return datetime.datetime.now().strftime('%H:%M:%S')

def get_answer(question, rag_mode, llm_mode):
    with console.status("[bold green]詢問中...") as status:
        answer = query(question, rag_mode, llm_mode)
    
    return answer

def handle_question(question, rag_mode, llm_mode):
    console.print()
    console.print('[medium_purple4][{0}] 😎 : [/]{1}'.format(timestamp(), question))
    console.print()
    console.print('[medium_purple4][{0}] 🤖 : [/]{1}'.format(timestamp(), get_answer(question, rag_mode, llm_mode)))
    console.print()

def main():
    rag_mode = RAG_MODE['rag_off']
    llm_mode = LLM_MODE['openai']

    question = console.input('[bold deep_sky_blue1]請輸入問題 [light_slate_grey]({0}, {1})[/] 🌳 : [/]'.format(rag_mode, llm_mode))
    
    while True:
        q = question.lower().strip()
        if q == 'help':
            console.print('\n指令：', style='hot_pink2')
            console.print('\trag on', style='rosy_brown')
            console.print('\trag off', style='rosy_brown')
            console.print('\trag only', style='rosy_brown')
            console.print()
            console.print('\topenai', style='dark_khaki')
            console.print('\tllama2', style='dark_khaki')
            console.print()
        elif q == 'exit' or q == 'quit':
            console.print('👋')
            quit()
        elif q == 'rag on':
            rag_mode = RAG_MODE['rag_on']
        elif q == 'rag off':
            rag_mode = RAG_MODE['rag_off']
        elif q == 'rag only':
            rag_mode = RAG_MODE['rag_only']
        elif q == 'openai':
            llm_mode = LLM_MODE['openai']
        elif q == 'llama2':
            llm_mode = LLM_MODE['llama2']
        else:
            handle_question(question, rag_mode, llm_mode)
        
        question = console.input('[bold deep_sky_blue1]請輸入問題 [light_slate_grey]({0}, {1})[/] 🌳 : [/]'.format(rag_mode, llm_mode))

if __name__ == '__main__':
    main()
