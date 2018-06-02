# Ваша задача построить сеть для произвольного семантического поля, где узлами будут слова,
# а ребрами наличие косинусного расстояния больше 0.5 в word2vec-модели.
# Вычислите самые центральные слова графа, его радиус (для каждой компоненты связности) и коэффициент кластеризации.


import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import networkx as nx
import matplotlib.pyplot as plt


# запускаем модель
def run_model():
    m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    model.init_sims(replace=True)
    return model


# ищем слова в модели, в словарь записываем для каждого слова расстояние до каждого другого слова
def get_distance():
    model = run_model()
    s_field = ["дождь_NOUN", "гроза_NOUN", "ненастье_NOUN", "непогода_NOUN", "молния_NOUN", "гром_NOUN", "ливень_NOUN",
               "снег_NOUN", "погода_NOUN", "солнце_NOUN", "туча_NOUN", "облако_NOUN"]
    dict_words = {}
    for word in s_field:
        if word in model:
            dict_distances = {}
            for w in s_field:
                if w != word:
                    dict_distances[w] = model.similarity(word, w)
            dict_words[word] = dict_distances

    return dict_words


# берем каждое слово из словаря, берем каждое слово из списка его значений, берем для этого слова его значение
# если оно больше 0.5, записываем в список так: (слово из словаря, слово из списка значений)
def define_edges(dict_words):
    edges = []
    for word in dict_words.keys():
        dict_distances = dict_words[word]
        for other_word in dict_distances.keys():
            if dict_distances[other_word] >= 0.5:
                edges.append((word, other_word))
    return edges


def get_graph(dict_words):
    nodes = []
    edges = define_edges(dict_words)
    print(edges)
    for key in dict_words.keys():
        nodes.append(key)
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph


def draw_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_color='black', node_size=50)
    nx.draw_networkx_edges(graph, pos, edge_color='green')
    nx.draw_networkx_labels(graph, pos, font_size=20, font_family='Arial')
    plt.axis('off')
    plt.savefig('graph.png')


def find_center(graph):
    deg = nx.degree_centrality(graph)
    sorted_nodes = sorted(deg, key=deg.get, reverse=True)
    return sorted_nodes[0]


def main():
    dict_words = get_distance()
    graph = get_graph(dict_words)
    draw_graph(graph)
    print(find_center(graph))
    print(nx.radius(graph))
    print(nx.average_clustering(graph))


if __name__ == "__main__":
    main()

