import time

def query(question, rag_mode, llm_mode):
    time.sleep(3)
    return '{0} {1} {2}'.format(question, rag_mode, llm_mode);

def main():
    query(input(), 'RAG ON', 'OPENAI')

if __name__ == '__main__':
    main()