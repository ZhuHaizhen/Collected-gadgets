library(KEGGREST)

orthologies <- keggList('orthology')

res <- data.frame('ko' = 0, 'name' = 0, 'description' = 0, 'pathway_id' = 0, 'pathway' = 0, 'class' = 0)
res <- res[-1, ]

for(i in 1:length(strsplit(orthologies, '\n'))){
  orth <- strsplit(orthologies, '\n')[i]
  ko_entry <- names(orth)
  ko_id <- strsplit(ko_entry, ':')[[1]][2]
  ko_des <- orth[[1]]
  ko_name <- strsplit(ko_des, ';')[[1]][1]
  ko_func <- strsplit(ko_des, ';')[[1]][2]
  ko_info <- keggGet(ko_entry)
  temp <- data.frame('ko' = 0, 'name' = 0, 'description' = 0, 'pathway_id' = 0, 'pathway' = 0, 'class' = 0)
  temp <- res[-1, ]
  
  if(length(ko_info[[1]]$PATHWAY) != 0){
    maps <- ko_info[[1]]$PATHWAY
    for(j in 1:length(strsplit(maps, '\n'))){
      map <- strsplit(maps, '\n')[j]
      map_id <- names(map)
      map_name <- map[[1]]
      map_entry <- paste('path:', map_id, sep = '')
      map_info <- keggGet(map_entry)
      if(length(map_info[[1]]$CLASS) > 0){
        map_class <- map_info[[1]]$CLASS
      }else{
        map_class <- 0
      }
      temp_sub <- data.frame('ko' = ko_id, 'name' = ko_name, 'description' = ko_func, 'pathway_id' = map_id, 'pathway' = map_name, 'class' = map_class)
      temp <- rbind(temp, temp_sub)
    }
  }else{
    temp  <- data.frame('ko' = ko_id, 'name' = ko_name, 'description' = ko_func, 'pathway_id' = 0, 'pathway' = 0, 'class' = 0)
  }
  res <- rbind(res, temp)
}