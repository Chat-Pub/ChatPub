from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('jhgan/ko-sroberta-multitask')

def set_index(data_list):
    # dim size
    d = 768

    # set index
    index = faiss.IndexFlatL2(d)
    Index = faiss.IndexIDMap2(index)

    # add the items into Index
    for item in data_list:
        id = item['YP']
        content = f"제목: {item['title']}\n"
        content += f"지원내용: {item['contents']['short_description']}\n"

        qualification = item['contents']['qualification']
        for key, value in qualification.items():
            if value != '-':
                content += f'{key}: {value}\n'

        content_vector = model.encode([content])
        vector_id = np.array([id], dtype='int64')
        Index.add_with_ids(content_vector, vector_id)
    
    return Index

def get_context(index, query, k, data_list):
    query_vector = model.encode([query])
    distance, index = index.search(query_vector, k)
    
    context= ""
    title_url_lists = []
    # idx shape: [query 개수, k]
    # shape: (1, k)
    for i in index[0]:
        title_url_item = {}
        for key, value in data_list[i].items():
            if key == 'title':
                context += f"제목: {value}\n"

                title_url_item['title'] = value
            
            elif key == 'contents':
                context += f"설명 요약: {value['short_description']}\n"
                context += f"요약: {value['summary']}\n"
                context += f"자격요건: {value['qualification']}\n"
                context += f"신청방법: {value['methods']}\n"

                title_url_item['url'] = value['url']

        title_url_lists.append(title_url_item)
        
        context += "##############################\n"
    
    return context, title_url_lists


def compute_similarity(response, title):
    preprocessed_response = response.replace('"','').replace("'",'').replace('\n', ' ').replace('  ', ' ')
    preprocessed_title = title.replace('"','').replace("'",'').replace('\n', ' ').replace('  ', ' ')
    tokenized_response = set(preprocessed_response.split(' '))
    tokenized_title = set(preprocessed_title.split(' '))

    return len(tokenized_title.intersection(tokenized_response)) / len(tokenized_title)

def get_valid_references(response, title_url_lists):
    references = ''

    for title_url_item in title_url_lists:
        title = title_url_item['title']
        url = title_url_item['url']
        
        sim = compute_similarity(response=response, title=title)

        if sim >= 0.5:
            if references != "":
                references += '\n'
            references += f'제목: {title}\n링크:{url}\n'

    return references
    