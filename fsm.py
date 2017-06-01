from transitions.extensions import GraphMachine
import tmdbsimple as tmdb
tmdb.API_KEY = '164de636f92ccc9e6587bf118fb26d8d'
string = ''

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        check = 0 
        if 'search' in text.lower():
            global string 
            str_tmp=text.lower()
            string=str_tmp.split('search')
            string=string[1]
            check = 1
        return check

    def is_going_to_state2(self, update):
        text = update.message.text
        check = 0 
        if 'upcoming' in text.lower():
            check=1
        return check

    def is_going_to_state3(self, update):
        text = update.message.text
        check = 0 
        if 'playing' in text.lower() and 'now' in text.lower():
            check=1
        return check

    def is_going_to_state4(self, update):
        text = update.message.text
        check = 0 
        if 'popular' in text.lower():
            check=1
        return check

    def is_going_to_state5(self, update):
        text = update.message.text
        check = 0 
        if 'yes' in text.lower():
            check=1
        return check
 
    def is_going_to_state6(self, update):
        text = update.message.text
        return text.lower() == 'no'   
    
    def is_going_to_state7(self, update):
        text = update.message.text
        if 'yes' in text.lower():
            return 1
        elif 'no' in text.lower():
            self.go_back(update)
    
    def is_going_to_state8(self, update):
        text = update.message.text
        global string 
        string=text.lower()
        check=0
        if text.lower():
            check=1
        return check

    def is_going_to_state9(self, update):
        text = update.message.text
        if 'yes' in text.lower():
            return 1
        elif 'no' in text.lower():
            self.go_back(update)
    
    def is_going_to_state10(self, update):
        text = update.message.text
        global string 
        string=text.lower()
        check=0
        if text.lower():
            check=1
        return check
    
    def on_enter_state1(self, update):
        search = tmdb.Search()
        response = search.movie(query=string)
        msg=''
        for s in search.results:
            msg=msg+s['title']+'\n'
        update.message.reply_text(msg)
        self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        movie = tmdb.Movies()
        response = movie.upcoming()
        lists=response['results']
        msg='There are several movies upcoming now.\n\n'
        update.message.reply_text(msg)
        for s in lists:
            msg=''
            msg=msg+'https://image.tmdb.org/t/p/w500'
            msg=msg+s['poster_path']
            update.message.reply_photo(msg)
            msg=s['title']+'\n'
            update.message.reply_text(msg)
        update.message.reply_text('Do you want to get more information?(YES or NO)')

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        movie = tmdb.Movies()
        response = movie.now_playing()
        lists=response['results']
        msg='There are several movies playing now.\n\n'
        update.message.reply_text(msg)
        for s in lists:
            msg=''
            msg=msg+'https://image.tmdb.org/t/p/w500'
            msg=msg+s['poster_path']
            update.message.reply_photo(msg)
            msg=s['title']+'\n'
            update.message.reply_text(msg)
        update.message.reply_text('Do you want to get more information?(YES or NO)')
    
    def on_exit_state3(self, update):
        print('Leaving state3')
    
    def on_enter_state4(self, update):
        update.message.reply_text("Playing in theater now?(YES or NO)")

    def on_exit_state4(self, update):
        print('Leaving state4')
    
    def on_enter_state5(self, update):
        movie = tmdb.Movies()
        response = movie.now_playing()
        lists=response['results']
        movie=''
        poster=''
        popular=0.0
        msg='This is the most popular movie playing in the theater now.\n\n'
        update.message.reply_text(msg)
        for s in lists:
            if s['popularity'] > popular:
                popular=s['popularity']
                movie=s['title']
                poster='https://image.tmdb.org/t/p/w500'+s['poster_path']
        update.message.reply_photo(poster)
        update.message.reply_text(movie)
        self.go_back(update)
    
    def on_exit_state5(self, update):
        print('Leaving state5')


    def on_enter_state6(self, update):
        movie = tmdb.Movies()
        response = movie.popular()
        lists=response['results']
        msg='This are several popular movies recently\n\n'
        update.message.reply_text(msg)
        for s in lists:
            msg=''
            msg=msg+'https://image.tmdb.org/t/p/w500'
            msg=msg+s['poster_path']
            update.message.reply_photo(msg)
            msg=s['title']+'\n'
            update.message.reply_text(msg)
        self.go_back(update)
    
    def on_exit_state6(self, update):
        print('Leaving state6')
    
    def on_enter_state7(self, update):
        update.message.reply_text("Which movie do you want to know?(enter a movie name)")
    
    def on_exit_state7(self, update):
        print('Leaving state7')
    
    def on_enter_state8(self, update):
        movie = tmdb.Movies()
        response = movie.now_playing()
        lists=response['results']
        msg=''
        for s in lists:
            if s['title'].lower() == string:
                movie_id=s['id']
                info = tmdb.Movies(movie_id).info()
                msg='https://image.tmdb.org/t/p/w500'
                msg=msg+info['poster_path']
                update.message.reply_photo(msg)
                msg=info['title']+'\n'
                update.message.reply_text(msg)
                msg='Overview:\n'+info['overview']
                update.message.reply_text(msg)
                msg='Runtime:\n'+str(info['runtime'])+'mins\n'
                update.message.reply_text(msg)
                genre = info['genres']
                msg='Genre:\n'
                for a in genre:
                    msg=msg+a['name']+'  '
                msg=msg+'\n'
                update.message.reply_text(msg)
                msg='Homepage:\n'+info['homepage']
                update.message.reply_text(msg)
                company = info['production_companies']
                msg='Companys:\n'
                for a in company:
                    msg=msg+a['name']+'\n'
                update.message.reply_text(msg)
                country = info['production_countries']
                msg='Production Countries:\n'
                for a in country:
                    msg=msg+a['name']+'\n'
                update.message.reply_text(msg)
                response1 = tmdb.Movies(movie_id).similar_movies()
                similar = response1['results']
                msg='Similar movies:\n'
                update.message.reply_text(msg)
                for s1 in similar:
                    msg='https://image.tmdb.org/t/p/w500'
                    msg=msg+s1['poster_path']
                    update.message.reply_photo(msg)
        self.go_back(update)
    
    def on_exit_state8(self, update):
        print('Leaving state8')
    
    def on_enter_state9(self, update):
        update.message.reply_text("Which movie do you want to know?(enter a movie name)")
    
    def on_exit_state9(self, update):
        print('Leaving state9')
    
    def on_enter_state10(self, update):
        movie = tmdb.Movies()
        response = movie.upcoming()
        lists=response['results']
        msg=''
        for s in lists:
            if s['title'].lower() == string:
                movie_id=s['id']
                info = tmdb.Movies(movie_id).info()
                msg='https://image.tmdb.org/t/p/w500'
                msg=msg+info['poster_path']
                update.message.reply_photo(msg)
                msg=info['title']+'\n'
                update.message.reply_text(msg)
                msg='Overview:\n'+info['overview']
                update.message.reply_text(msg)
                msg='Runtime:\n'+str(info['runtime'])+'mins\n'
                update.message.reply_text(msg)
                genre = info['genres']
                msg='Genre:\n'
                for a in genre:
                    msg=msg+a['name']+'  '
                msg=msg+'\n'
                update.message.reply_text(msg)
                msg='Homepage:\n'+info['homepage']
                update.message.reply_text(msg)
                company = info['production_companies']
                msg='Companys:\n'
                for a in company:
                    msg=msg+a['name']+'\n'
                update.message.reply_text(msg)
                country = info['production_countries']
                msg='Production Countries:\n'
                for a in country:
                    msg=msg+a['name']+'\n'
                update.message.reply_text(msg)
                response1 = tmdb.Movies(movie_id).similar_movies()
                similar = response1['results']
                msg='Similar movies:\n'
                update.message.reply_text(msg)
                for s1 in similar:
                    msg='https://image.tmdb.org/t/p/w500'
                    msg=msg+s1['poster_path']
                    update.message.reply_photo(msg)
        self.go_back(update)
    
    def on_exit_state10(self, update):
        print('Leaving state10')
