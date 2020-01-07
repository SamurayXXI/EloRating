# EloRating

# Профилирование запуск  
python3 manage.py runprofileserver --use-cprofile --prof-path=/tmp/prof/  
  
# Профиирование создание дерева вызовов  
gprof2dot -f pstats /tmp/prof/last_matches_fill.013204ms.1578437510.prof | dot -Tpng -o last_matches.png  
  
# Профилирование 
snakeviz /tmp/prof/last_matches_fill.013204ms.1578437510.prof   
