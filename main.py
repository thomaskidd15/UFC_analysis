import pandas as pd
import matplotlib.pyplot as plt


class UFCAnalysis:

    def __init__(self):
        self.events_table = pd.read_csv('./data/events.csv')
        self.fighters_table = pd.read_csv('./data/fighters.csv')
        self.fights_table = pd.read_csv('./data/fights.csv')
        self.stats_table = pd.read_csv('./data/stats.csv')

        # TASK 1 (DATA PREPARATION) CODE HERE
      
        self.stats_table = self.stats_table.loc[~self.stats_table['result'].isna(), :]
        self.fights_table = self.fights_table.loc[~self.fights_table['winner'].isna(), :]

        self.events_table['date'] = pd.to_datetime(self.events_table['date'])
        self.fighters_table['dob'] = pd.to_datetime(self.fighters_table['dob'])

    def question_1(self) -> None:
        """ which fighters have the most wins and losses? """
        
        results_count = self.stats_table.groupby(['fighter', 'result']).size().unstack(fill_value=0)

        if 'win' in results_count.columns:
            most_wins = results_count['win'].idxmax()
            max_wins = results_count['win'].max()
            print(f'{most_wins}: {max_wins}')

        fighter_losses = results_count.loc[most_wins]['loss'] if 'loss' in results_count.columns else 0

        fig, ax = plt.subplots()
        ax.bar(['Wins', 'Losses'], [max_wins, fighter_losses], color=['green', 'red'])
        ax.set_title(f'Wins and Losses for Fighter: {most_wins}')
        ax.set_xlabel('Result')
        ax.set_ylabel('Number of Fights')
        plt.show()


        if 'loss' in results_count.columns:
            most_losses = results_count['loss'].idxmax()
            max_losses = results_count['loss'].max()
            print(f'{most_losses}: {max_losses}')

    def question_3(self) -> None:
        """ is there an age advantage? """
        self.fighters_table = self.fighters_table.loc[~self.fighters_table['dob'].isna(), :]

        fighters_with_birthdays = self.stats_table.merge(self.fighters_table[['name', 'dob']], left_on='fighter', right_on='name', how='left')
        fighteropponent_with_birthdays = fighters_with_birthdays.merge(self.fighters_table[['name', 'dob']], left_on='opponent', right_on='name', how='left')
        
        fighteropponent_with_birthdays['age_diff'] = fighteropponent_with_birthdays['dob_x'] - fighteropponent_with_birthdays['dob_y']
        fighteropponent = fighteropponent_with_birthdays.dropna(subset=['dob_x', 'dob_y'])

        fighteropponent.loc[:,'numberic_result'] = fighteropponent['result'].map({'win': 1, 'loss': 0})  # I tried to use this .loc[:, to get rid of the warnign message nothing changed
        s1 = fighteropponent['age_diff']
        s2 = fighteropponent['numberic_result']

        # print(s1.corr(s2))

        print(f'The correlation coefficient: {s1.corr(s2)} tells us that there is a weak positive relationship between being older than your opponent and winning a fight. Meaning, older fighters tend to have a slightly higher chance of winning, but the effect is not strong.')


    def question_4(self) -> None:
        """ is there a stance advantage? """
        
        self.fighters_table = self.fighters_table.loc[~self.fighters_table['dob'].isna(), :]

        fighters_with_stance = self.stats_table.merge(self.fighters_table[['name', 'stance']], left_on='fighter', right_on='name', how='left')

        fighters_with_stance.loc[:,'numberic_result'] = fighters_with_stance['result'].map({'win': 1, 'loss': 0})
        fighters_with_stance = fighters_with_stance[fighters_with_stance['stance'] != 'Open Stance']

        fighters_with_stance['stance_group'] = fighters_with_stance['stance'].apply(
            lambda x: 'Southpaw/Switch' if x in ['Southpaw', 'Switch'] else 'Orthodox')

        name_stance_result = fighters_with_stance.groupby('stance_group')['numberic_result'].mean()
        
        print('Win Outcomes Precentage in decimal form')
        print(f"Orthodox: {name_stance_result['Orthodox']:.3f}")
        print(f"Southpaw/Switch: {name_stance_result['Southpaw/Switch']:.3f}")
      
    def question_6(self) -> None:
        """ Which fighter has dealt the most strikes to a specific opponent? """
        
        
        agg_stats = self.stats_table.groupby(['fighter', 'opponent']).agg(
        total_strikes=('sig. str.', 'sum'),
        num_fight=('sig. str.', 'count')
    )
    
        top_fight = agg_stats.sort_values(by='total_strikes', ascending=False).head(1)
    
        fighter = top_fight.index[0][0]
        opponent = top_fight.index[0][1]
        total_strikes = top_fight['total_strikes'].values[0]
        num_fights = top_fight['num_fight'].values[0]

        print(f'Fighter: {fighter}, Opponent: {opponent}, Total Strikes: {total_strikes}, Number of Fights: {num_fights}')


    def question_7(self) -> None:
        """ which fighter has had the longest career? """

        fights_with_dates = self.fights_table.merge(self.events_table[['event', 'date']], on='event', how='left')

        fighter1 = fights_with_dates[['fighter1', 'date']].rename(columns={'fighter1': 'fighter'})
        fighter2 = fights_with_dates[['fighter2', 'date']].rename(columns={'fighter2': 'fighter'})

        all_fights = pd.concat([fighter1, fighter2])

        career_span = all_fights.groupby('fighter')['date'].agg(['min', 'max'])
        career_span['length_days'] = (career_span['max'] - career_span['min']).dt.days

        longest_fighter = career_span['length_days'].idxmax()
        longest_length = career_span.loc[longest_fighter, 'length_days']

        print(f'{longest_fighter}: {longest_length}')


# Testing
ufc = UFCAnalysis()
ufc.question_1()
'\n'
ufc.question_2()
'\n'
ufc.question_3()
'\n'
ufc.question_4()
'\n'
ufc.question_5()
'\n'
ufc.question_6()
'\n'
ufc.question_7()
