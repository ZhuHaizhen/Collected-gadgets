#if(!requireNamespace('BiocManager', quietly = TRUE))      
#  install.packages('BiocManager') 
#BiocManager::install('KEGGREST') 

library('KEGGREST')

pathways <- keggList('pathway')

res <- data.frame('ko' = 0, 'name' = 0, 'description' = 0, 'module_id' = 0, 'module' = 0, 'pathway_id' = 0, 'pathway' = 0, 'class' = 0)
res <- res[-1, ]

# 遍历所有map
for(i in 1: length(strsplit(pathways, '\n'))){
  pathway <- strsplit(pathways, '\n')[i]
#  print(pathway)}
  map_entry <- names(pathway)
#  print(map_entry)}
  map_name <- pathway[[1]]
  map_info <- keggGet(map_entry)
  map_id <- map_info[[1]]$KO_PATHWAY
  # 处理缺少分类的情况
  if(length(map_info[[1]]$CLASS != 0)){
    map_class <- map_info[[1]]$CLASS
  }
  else{
    map_class <- 'None'
  }
  # 提取map中的模块
  modules <- map_info[[1]]$MODULE
  # 处理不包含模块的map
  if(length(modules) != 0){
    # 遍历map中的模块
    for(j in 1: length(strsplit(modules, '\n'))){
      module <- strsplit(modules, '\n')[j]
      module_id <- names(module)
      module_name <- module[[1]]
      module_entry <- paste('module:', module_id, sep = '')
      module_info <- keggGet(module_entry)
      orthologies <- module_info[[1]]$ORTHOLOGY
      # 遍历模块中的ko
      for(k in 1: length(strsplit(orthologies, '\n'))){
        ko <- strsplit(orthologies, '\n')[k]
        # 处理多个ko对应同一功能的情况
        if(length(strsplit(names(ko), ',')[[1]]) > 1){
          for(kos in strsplit(names(ko), ',')){
            # 处理ko编号带有其它信息的情况
            if(startsWith(kos, 'K')){
              ko_entry <- paste('orthology:', substr(kos, 1, 6), sep = '')
              ko_info <- keggGet(ko_entry)
              ko_name <- ko_info[[1]]$NAME
              ko_description <- ko_info[[1]]$DEFINITION
              temp <- data.frame('ko' = kos, 'name' = ko_name, 'description' = ko_description, 'module_id' = module_id, 'module' = module_name, 'pathway_id' = map_id, 'pathway' = map_name, 'class' = map_class)
              res <- rbind(res, temp)
            }
            else{
              next
            }
          }
        }else{
          ko_id <- names(ko)
          ko_entry <- paste('orthology:', ko_id, sep = '')
          ko_info <- keggGet(ko_entry)
          ko_name <- ko_info[[1]]$NAME
          ko_description <- ko_info[[1]]$DEFINITION
          temp <- data.frame('ko' = kos, 'name' = ko_name, 'description' = ko_description, 'module_id' = module_id, 'module' = module_name, 'pathway_id' = map_id, 'pathway' = map_name, 'class' = map_class)
          res <- rbind(res, temp)
        }
      }
    }
  }else{
    next
  }
}

write.table(res, 'kos_API.txt', quote = F, sep = '\t', row.names = F)
