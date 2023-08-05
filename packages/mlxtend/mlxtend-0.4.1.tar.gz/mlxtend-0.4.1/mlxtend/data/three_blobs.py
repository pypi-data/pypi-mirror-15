# Sebastian Raschka 2014-2016
# mlxtend Machine Learning Library Extensions
#
# A function for loading a sample dataset for clustering evaluations
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause

import numpy as np


def three_blobs_data():
    """A random dataset of 3 2D blobs for clustering.

    Number of samples : 150
    Suggested labels : {0, 1, 2}, distribution: [50, 50, 50]

    Returns
    --------
    X, y : [n_samples, n_features], [n_cluster_labels]
        X is the feature matrix with 159 samples as rows
        and 2 feature columns.
        y is a 1-dimensional array of the 3 suggested cluster labels 0, 1, 2

    """
    X = np.array([
                  [2.60509732, 1.22529553],
                  [0.5323772, 3.31338909],
                  [0.802314, 4.38196181],
                  [0.5285368, 4.49723858],
                  [2.61858548, 0.35769791],
                  [1.59141542, 4.90497725],
                  [1.74265969, 5.03846671],
                  [2.37533328, 0.08918564],
                  [-2.12133364, 2.66447408],
                  [1.72039618, 5.25173192],
                  [3.1368855, 1.56592763],
                  [-0.37494566, 2.38787435],
                  [-1.84562253, 2.71924635],
                  [0.72144399, 4.08475018],
                  [0.16117091, 4.53517846],
                  [-1.99912714, 2.71285741],
                  [-1.47804153, 3.2093591],
                  [1.8706766, 0.77797407],
                  [-1.5933443, 2.76898682],
                  [2.03562611, 0.31361691],
                  [0.64003985, 4.12401075],
                  [2.4411628, 1.30941574],
                  [1.13280393, 3.87673946],
                  [1.04829186, 5.03092408],
                  [-1.26637157, 2.62998828],
                  [2.31690585, 0.81189049],
                  [2.36230721, 1.358767],
                  [1.2091013, 3.53566548],
                  [-2.54224625, 3.95012869],
                  [1.4815332, 0.67875364],
                  [-1.59487886, 3.48632794],
                  [-1.82556205, 2.7989214],
                  [-1.13374003, 2.68467271],
                  [-1.758702, 3.158623],
                  [0.3498724, 4.69253251],
                  [1.68548602, 1.66917096],
                  [2.989047, 1.35068599],
                  [1.73734448, 1.23588031],
                  [0.65910903, 4.12241674],
                  [1.15445328, 4.65707391],
                  [-1.32738084, 1.53158588],
                  [-1.6814105, 2.07988036],
                  [0.34102758, 4.78848568],
                  [1.87827057, 0.21018801],
                  [2.13860427, 1.21517938],
                  [2.48368283, 0.57215086],
                  [-1.18113464, 3.26525683],
                  [2.11114739, 3.57660449],
                  [-1.19371247, 2.68752237],
                  [1.45131429, 4.22810872],
                  [1.83769075, 1.82229552],
                  [0.44089377, 4.83101319],
                  [1.08040757, 4.79210685],
                  [1.84845803, 0.52393625],
                  [2.3914149, 1.10139458],
                  [-1.44865074, 3.03397278],
                  [0.72086751, 3.71347124],
                  [3.01673853, 1.63792106],
                  [-1.18199493, 3.56880538],
                  [1.34081536, 4.36827878],
                  [-2.31837321, 3.22307195],
                  [-0.54894786, 3.11292892],
                  [-1.6823471, 2.96658234],
                  [-1.53541422, 3.10745813],
                  [1.06498315, 4.10289686],
                  [-0.39724954, 2.89675369],
                  [1.03972612, 4.50478201],
                  [1.62465468, 1.85269614],
                  [-0.30022483, 4.63059663],
                  [0.12313498, 5.27917503],
                  [1.54597042, 3.68637442],
                  [1.44254976, 1.31984515],
                  [2.52889351, 0.82015861],
                  [0.38970838, 5.27559792],
                  [1.5381461, 1.23846092],
                  [0.82049381, 4.33187],
                  [1.56565986, 4.21382491],
                  [-1.93358614, 2.1846701],
                  [-1.38373217, 3.22230418],
                  [0.96217896, 4.51795326],
                  [1.71810119, 0.91357894],
                  [1.65356269, 0.55288877],
                  [0.4519936, 3.59377836],
                  [1.19820169, 4.47062449],
                  [2.20438661, 1.56085661],
                  [3.24683991, 1.3699034],
                  [2.51569693, 1.05702749],
                  [-1.79833475, 3.12590728],
                  [-2.0495307, 3.52345491],
                  [2.36788325, 0.09663483],
                  [2.24348029, 0.34796326],
                  [0.99914934, 4.2101954],
                  [1.30963873, 1.11735951],
                  [0.77468161, 4.91500986],
                  [1.70798359, 0.82284639],
                  [1.91784543, 3.6299078],
                  [-2.00487651, 2.74489137],
                  [-2.10499523, 3.30848131],
                  [1.39731382, 0.66687136],
                  [2.02114672, 1.75433502],
                  [1.67030948, 1.16728826],
                  [2.52997792, 0.94143928],
                  [-2.18016744, 3.7469476],
                  [2.00604126, 0.56592452],
                  [1.50307585, 0.9237462],
                  [1.05374379, 4.49286859],
                  [-1.72662853, 3.10291021],
                  [1.72330962, 4.2012082],
                  [0.92466065, 4.50908658],
                  [0.39369516, 4.75420057],
                  [-1.31377465, 3.25633628],
                  [0.78260667, 4.15263595],
                  [1.82750127, 0.90640324],
                  [-1.2649585, 2.9620933],
                  [0.98152009, 5.19672257],
                  [-2.49504392, 3.01227156],
                  [1.00952869, 4.45502328],
                  [1.40848818, 3.93270482],
                  [-1.28003312, 2.85983029],
                  [-1.82506103, 2.89159861],
                  [0.5408715, 4.0143625],
                  [2.64928242, 1.05613497],
                  [0.5226209, 4.32976003],
                  [0.16932115, 4.19741719],
                  [1.8062513, 1.86242969],
                  [1.92126584, 1.29889186],
                  [-1.53906708, 2.54886681],
                  [1.68289011, 0.48444439],
                  [-2.29730252, 2.94951326],
                  [-1.45592743, 2.75821805],
                  [-1.38694171, 2.86880707],
                  [-1.07181456, 3.07649137],
                  [1.40883907, 1.03118909],
                  [-1.58598604, 2.57779316],
                  [-1.58217434, 3.42796862],
                  [-0.77966174, 1.88288975],
                  [0.56969694, 3.44064603],
                  [-1.8531083, 2.72240557],
                  [1.59885641, 1.4561718],
                  [-1.84094779, 2.6773687],
                  [1.35678894, 4.36462484],
                  [1.1774409, 3.96138228],
                  [1.73345832, -0.21403792],
                  [2.34356293, 0.79351428],
                  [-0.95073823, 3.45769156],
                  [-2.23893447, 2.67122232],
                  [-1.87292894, 3.68607079],
                  [-1.8897027, 2.22620028],
                  [2.25327088, 0.35113291],
                  [1.55515985, 0.12527811]])

    y = np.array([1, 2, 2, 2, 1, 2, 2, 1, 0, 2, 1, 0, 0, 2, 2, 0, 0, 1,
                  0, 1, 2, 1, 2, 2, 0, 1, 1, 2, 0, 1, 0, 0, 0, 0, 2, 1,
                  1, 1, 2, 2, 0, 0, 2, 1, 1, 1, 0, 2, 0, 2, 1, 2, 2, 1,
                  1, 0, 2, 1, 0, 2, 0, 0, 0, 0, 2, 0, 2, 1, 2, 2, 2, 1,
                  1, 2, 1, 2, 2, 0, 0, 2, 1, 1, 2, 2, 1, 1, 1, 0, 0, 1,
                  1, 2, 1, 2, 1, 2, 0, 0, 1, 1, 1, 1, 0, 1, 1, 2, 0, 2,
                  2, 2, 0, 2, 1, 0, 2, 0, 2, 2, 0, 0, 2, 1, 2, 2, 1, 1,
                  0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 1, 0, 2, 2, 1, 1,
                  0, 0, 0, 0, 1, 1])

    return X, y
