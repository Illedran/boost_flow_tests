#include <boost/config.hpp>
#include <iostream>
#include <fstream>
#include <string>
#include <boost/graph/edmonds_karp_max_flow.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/read_dimacs.hpp>
#include <boost/graph/graph_utility.hpp>
#include <stack>
#include <utility>
#include <algorithm>

using namespace boost;

typedef adjacency_list_traits<vecS, vecS, directedS> Traits;
typedef adjacency_list<listS, vecS, directedS,
                       property<vertex_name_t, std::string>,
                       property<edge_capacity_t, long,
                                property<edge_residual_capacity_t,
                                         long,
                                         property<edge_reverse_t,
                                                  Traits::edge_descriptor> > > >
    Graph;


void flow_dfs (const Graph &g, Graph::vertex_descriptor vertex, int t, int i, std::vector<std::vector< int> >& paths, const property_map<Graph, edge_capacity_t>::type &capacity, const property_map<Graph, edge_residual_capacity_t>::type &residual_capacity) {
//    if(vertex == t){
//        paths[i].push_back(t);
//    }
//    else {
        Graph::out_edge_iterator ei, e_end;
        for (boost::tie(ei, e_end) = out_edges(vertex, g); ei != e_end; ++ei) {
            if (capacity[*ei] - residual_capacity[*ei] > 0) {
                paths[i].push_back(vertex);
                flow_dfs(g,
                         (*ei).m_target,
                         t,
                         i,
                         paths,
                         capacity,
                         residual_capacity);
            }
        }
//    }
}

int
main() {


    Graph g;

    property_map<Graph, edge_capacity_t>::type capacity = get(edge_capacity, g);
    property_map<Graph, edge_reverse_t>::type rev = get(edge_reverse, g);
    property_map<Graph, edge_residual_capacity_t>::type
        residual_capacity = get(edge_residual_capacity, g);


    std::ifstream in("./sample_data/sample_1024-10_1-256.txt");
    int n, m, s, t;
    in >> n >> m >> s >> t;
    for (int i = 0; i < n; i++) {
        boost::add_vertex(g);
    }
    for (int i = 0; i < m; i++) {
        Traits::edge_descriptor e, e_rev;
        bool added;
        int from, to, cap_value;
        in >> from >> to >> cap_value;
        boost::tie(e, added) = boost::add_edge(from, to, g);
        boost::tie(e_rev, added) = boost::add_edge(to, from, g);
        capacity[e] = 1;
        capacity[e_rev] = 0;
        rev[e] = e_rev;
        rev[e_rev] = e_rev;
    }

    long flow = edmonds_karp_max_flow(g, s, t);
    std::cout << flow << std::endl;
    Graph::out_edge_iterator ei, e_end;
    std::vector<std::vector<int > > paths (flow);
    int i = 0;
    for (boost::tie(ei, e_end) = out_edges(s, g); ei != e_end; ++ei){
        if (capacity[*ei] - residual_capacity[*ei] > 0) {
//          paths[i].push_back(s);
            flow_dfs(g, (*ei).m_target, t, i, paths, capacity, residual_capacity);
        }
        i++;
    }
    for(int i = 0; i<flow; i++){
        for(int j = 0; j < paths[i].size(); j++){
            std::cout << paths[i][j] << " ";
        }
        std::cout << std::endl;
    }
    return EXIT_SUCCESS;
}

