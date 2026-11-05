// Número de Pokémon
db.Pokemon.find().count()

// Número de Pokémon sin evolución
db.Pokemon.find({'next_evolution': {$exists: false}}).count()

// Número de tipos de Pokémon
db.Pokemon.aggregate([{$unwind: '$type'},
                        {$group: {_id: '$type', Total: {$sum: 1}}},
                        {$sort: {Total: -1}}])
                        
// 5 debilidades más comunes
db.Pokemon.aggregate([{$unwind: '$weaknesses'},
                        {$group: {_id: '$weaknesses', Total: {$sum: 1}}},
                        {$sort: {Total: -1}},
                       {$limit: 5}])

// Pokémon más alto
db.Pokemon.find({},{_id: 0, 'name': 1, 'height': 1}).sort({height: -1}).limit(1)

// Pokémon más bajo
db.Pokemon.find({},{_id: 0,'name': 1, 'height': 1}).sort({height: 1}).limit(1)

// Pokémon más pesado
db.Pokemon.find({},{_id: 0,'name': 1, 'weight': 1}).sort({weight: -1}).limit(1) 

// Pokémon más ligero
db.Pokemon.find({},{_id: 0,'name': 1, 'weight': 1}).sort({weight: 1}).limit(1) 

// Número de Pokémon encontrados en cada tipo de huevo
db.Pokemon.aggregate([{$group: {_id: '$egg', Total: {$sum: 1}}},
                       {$sort: {Total: -1}}])

// Número de Pokémon según el tipo de caramelo
db.Pokemon.aggregate([{$group: {_id: '$candy', Total: {$sum: 1}}},
                        {$sort: {Total: -1}}])                       


// Media de caramelos necesarios para cada Pokémon

 db.Pokemon.aggregate([{$unwind: '$type'},

                        {$group: {_id: '$type', Media: {$avg: '$candy_count'}}},

                        {$sort: {Media: -1}}])

                        
// Número de Pokémon con multiplicador nulo
db.Pokemon.find({multipliers: null}).count()

// Media de apariciones para cada tipo de Pokémon
db.Pokemon.aggregate([{$unwind: '$type'},
                        {$group: {_id: '$type', Media: {$avg: '$avg_spawns'}}},
                        {$sort: {Media: -1}}])

// Longitud media del nombre de los Pokémon
db.Pokemon.aggregate([{$project: {_id: '$name', 'length': {$strLenCP: '$name'}}},
                        {$group: {_id: null, Average_characters_in_name: {$avg: '$length'}}}])                
