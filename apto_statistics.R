graph_data <- read.csv("ns_data2019-06-07_21:42.csv", sep=',')
library(dplyr)
library(tidyr)
library(ggplot2)
library(ggthemes)
graph_data %>% head


# zależność czasu od rozmiaru drzewa   
# 1. Linie dla grafu zawierającego poddrzewo
  # a) linia dla grafu rzadkiego
  # b) linia dla graf gęstego
    
head(graph_data)
#graph_size = 30
sparse.graph <- graph_data %>% 
  filter(with_copy=="True", is_dense_graph=='False', graph_id=='a2b31d6fe10e45f585d6cf675a935764')

dense.graph <- graph_data %>% 
  filter(with_copy=="True", is_dense_graph=='True', graph_id=='01da78dab06f4ebaa1b155c3e49256c2') 

data_tree_dep <- data.frame(sparse.graph, dense.graph) %>% select(-tree_size.1) 

data_tree_dep %>% rename(
  sparse = time_meas,
  dense = time_meas.1 
) %>% gather(graph, time, sparse, dense ) %>% 
  ggplot(aes(x=tree_size, y=time, colour=graph)) +
  ggtitle('Time dependency on tree size for graph with tree copy') +
  geom_line() +
  theme_hc() +
  scale_fill_hc()

data_tree_dep %>% rename(
  sparse = mean_mem,
  dense = mean_mem.1 
) %>% gather(graph, memory, sparse, dense ) %>% 
  ggplot(aes(x=tree_size, y=memory, colour=graph)) +
  geom_line() +
  ggtitle('Memory dependency on tree size for graph with tree copy') +
  theme_hc() +
  scale_fill_hc() 

# 2. Linie dla grafu nie zawierającego poddrzewa

sparse.graph <- graph_data %>% 
  filter(with_copy=="False", is_dense_graph=='False', graph_id=='4f74dd304cb94c3f836539734ee5c8f6')

sparse.graph %>% rename(
  time = time_meas,
  memory=mean_mem
) %>% ggplot(aes(x=tree_size, y=time)) +
               geom_line() +
  ggtitle('Time dependency on tree size for graph without tree copy') +
  theme_hc() +
  scale_fill_hc()

  sparse.graph %>% rename(
  time = time_meas,
  memory=mean_mem
) %>% ggplot(aes(x=tree_size, y=memory)) +
               geom_line() +
  ggtitle('Memory dependency on tree size for graph without tree copy') +
  theme_hc() +
  scale_fill_hc()
# zależność pamięci od rozmiaru drzewa 
# 1. Linie dla grafu zawierającego poddrzewo
  # a) linia dla grafu rzadkiego
  # b) linia dla graf gęstego
# 2. Linie dla grafu nie zawierającego poddrzewa


# zależność czasu od rozmiaru grafu 
# 1. Linie dla grafu zawierającego poddrzewo
  # a) linia dla grafu rzadkiego
  # b) linia dla graf gęstego
# 2. Linie dla grafu nie zawierającego poddrzewa


sparse.graph <- graph_data %>% 
  filter(with_copy=="True", is_dense_graph=='False', 
         tree_id=='2e418b65a0764810aadcdc2e5ff9e805')

un_sparse.graph <- sparse.graph[-1,]


dense.graph <- graph_data %>% 
  filter(with_copy=="True", is_dense_graph=='True', 
         tree_id=='2e418b65a0764810aadcdc2e5ff9e805')

un_dense.graph <- dense.graph[-1,]

data_graph_dep <- data.frame(un_sparse.graph, un_dense.graph) %>% select(-tree_size.1) 

data_graph_dep %>% rename(
  sparse = time_meas,
  dense = time_meas.1 
) %>% gather(graph, time, sparse, dense ) %>% 
  ggplot(aes(x=graph_size, y=time, colour=graph)) +
  geom_line() +
  ggtitle("Time dependency on graph size with tree copy") +
  theme_hc() +
  scale_fill_hc()

data_graph_dep %>% rename(
  sparse = mean_mem,
  dense = mean_mem.1 
) %>% gather(graph, memory, sparse, dense ) %>% 
  ggplot(aes(x=graph_size, y=memory, colour=graph)) +
  geom_line() +
  ggtitle("Memory dependency on graph size with tree copy") +
  theme_hc() +
  scale_fill_hc()

# 2. Linie dla grafu nie zawierającego poddrzewa

sparse.graph <- graph_data %>% 
  filter(with_copy=="False", tree_id=='2e418b65a0764810aadcdc2e5ff9e805')

un_sparse.graph <- sparse.graph[-5,]

un_sparse.graph %>% rename(
  time = time_meas,
  memory=mean_mem
) %>% ggplot(aes(x=graph_size, y=time)) +
               geom_line() +
  ggtitle("Time dependency on graph size without tree copy") +
  theme_hc() +
  scale_fill_hc()

un_sparse.graph %>% rename(
  time = time_meas,
  memory=mean_mem
) %>% ggplot(aes(x=graph_size, y=memory)) +
               geom_line() +
  ggtitle("Memory dependency on graph size without tree copy") +
  theme_hc() +
  scale_fill_hc()

# zależność pamięci od rozmiaru grafu 
# 1. Linie dla grafu zawierającego poddrzewo
  # a) linia dla grafu rzadkiego
  # b) linia dla graf gęstego
# 2. Linie dla grafu nie zawierającego poddrzewa