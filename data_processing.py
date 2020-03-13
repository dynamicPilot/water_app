import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import datetime

import config as c

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class DataProcessing():
    def __init__(self):
        self.data_path = c.data_path
        self.file_save_path = c.file_save_path
        self.data = None
        
        self.cold_water_price = c.cold_water_price
        self.hot_water_price = c.hot_water_price
        self.month_number_to_plot = c.month_number_to_plot
        self.last_cvs_value = 0
        self.last_hvs_value = 0

        self.month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
        'August', 'September', 'October', 'November', 'December']
        self.month_mapping_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 
        'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        self.month_mapping_shorter_dict = {'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr', 'May':'May', 'June': 'Jun', 'July': 'Jul', 
        'August': 'Aug', 'September':'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec'}

        self.data_loader()

    def data_loader(self):
        self.data = pd.read_csv(self.data_path, sep = '\t', header=0)

        if len(self.data) < self.month_number_to_plot:
            self.month_number_to_plot = len(self.data)

        self.last_cvs_value = self.data['CVS'].loc[len(self.data)-1]
        self.last_hvs_value = self.data['HVS'].loc[len(self.data)-1]
       

    def add_data(self, value_array):
        file_to_write = open(self.data_path, 'a')

        file_to_write.write('\n')
        file_to_write.write(value_array[0])
        file_to_write.write('\t')
        file_to_write.write('{:04d}'.format(int(value_array[1])))
        file_to_write.write('\t')
        file_to_write.write('{:.3f}'.format(float(value_array[2])))
        file_to_write.write('\t')
        file_to_write.write('{:.3f}'.format(float(value_array[3])))
        file_to_write.close()

        self.data_loader()

    def calculate_prices(self):
        self.data['DELTA_CVS'] = 0.00
        self.data['DELTA_HVS'] = 0.00
        self.data['PRICE_CVS'] = 0.00
        self.data['PRICE_HVS'] = 0.00
        self.data['TOTAL'] = 0.00
        for i in range(1, len(self.data)):
            self.data['DELTA_CVS'].loc[i] = self.data['CVS'].loc[i] - self.data['CVS'].loc[i-1]
            self.data['DELTA_HVS'].loc[i] = self.data['HVS'].loc[i] - self.data['HVS'].loc[i-1]
            self.data['PRICE_CVS'].loc[i] = self.data['DELTA_CVS'].loc[i] * self.cold_water_price
            self.data['PRICE_HVS'].loc[i] = self.data['DELTA_HVS'].loc[i] * self.hot_water_price
            self.data['TOTAL'].loc[i] =  self.data['PRICE_CVS'].loc[i] + self.data['PRICE_HVS'].loc[i]


    def data_to_new_value_analysis(self):
        self.calculate_prices()
        prediction = self.make_model_for_prediction()
        i = len(self.data)-1
        cvs_aver = [self.data['DELTA_CVS'].loc[:i].mean(), self.data['PRICE_CVS'].loc[:i].mean()]
        hvs_aver = [self.data['DELTA_HVS'].loc[:i].mean(), self.data['PRICE_HVS'].loc[:i].mean()]
        result_dict = {'month': self.data['MONTH'].loc[i], 
        'year': self.data['YEAR'].loc[i],
        'cvs': self.data['CVS'].loc[i],
        'hvs': self.data['HVS'].loc[i],
        'delta_cvs': self.data['DELTA_CVS'].loc[i],
        'delta_hvs': self.data['DELTA_HVS'].loc[i],
        'price_cvs': self.data['PRICE_CVS'].loc[i],
        'price_hvs': self.data['PRICE_HVS'].loc[i],
        'total': self.data['TOTAL'].loc[i],
        'cvs_aver': cvs_aver,
        'hvs_aver': hvs_aver,
        'total_aver': self.data['TOTAL'].loc[:i].mean(),
        'price_cvs_pred': prediction['cold'][0]*self.cold_water_price,
        'price_hvs_pred': prediction['hot'][0]*self.hot_water_price}

        self.create_graphs_to_new_value_analysis()
        return result_dict

    def create_graphs_to_new_value_analysis(self):
        #self.data_to_new_value_analysis()
        colors = ['#717D7E'] * (self.month_number_to_plot-1)+['#73C6B6']
        df_to_plot = self.data.iloc[len(self.data)-self.month_number_to_plot:].reset_index(drop=True)
        x_ticks = [i for i in range(self.month_number_to_plot)]
        x_labels = df_to_plot['MONTH'].map(self.month_mapping_shorter_dict).tolist()
        for tag in ['PRICE_CVS', 'PRICE_HVS', 'TOTAL']:

            fig = plt.figure(figsize = (10, 5), tight_layout = True)
            ax = fig.add_subplot()
            width = 0.9
            ax.bar(x_ticks, df_to_plot[tag], width, color = colors)
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_labels, size=25)
            ax.set_xlabel('Month', size=27)
            ax.set_ylabel('Price, rub', size=27)
            ax.tick_params(axis='y', labelsize=22)
            plt.savefig(f'temp/{tag}.png')
            #plt.show()

    def delete_last_line_in_file(self):
        with open(self.data_path, 'r') as f:
            lines = f.readlines()
            lines = lines[:-1]

        with open(self.data_path, 'w') as f:
            f.writelines(lines)

    def make_model_for_prediction(self):
        self.data['MONTH_MAPPED'] = self.data['MONTH'].map(self.month_mapping_dict)
        last_month = self.data['MONTH_MAPPED'].loc[len(self.data)-1]

        features = self.data[['MONTH_MAPPED']].iloc[1:]
        deltas = {'cold': self.data['DELTA_CVS'].iloc[1:], 'hot': self.data['DELTA_HVS'].iloc[1:]}
        prediction_for_three_month = {'cold': None, 'hot': None}
        self.models = {'cold': None, 'hot': None}

        for tag, delta in deltas.items():
            # Perform train, test, split
            train_set, test_set, train_labels, test_labels = train_test_split(features, delta, test_size = 0.2, random_state = 100)
            # Scale the feature data so it has mean = 0 and standard deviation = 1
            regular = StandardScaler()
            train_set = regular.fit_transform(train_set)
            test_set = regular.transform(test_set)
            # Create and train the models for cold water
            model = KNeighborsRegressor(n_neighbors=10, weights='distance')
            train_score = []
            test_score = []
            prediction = []

            model.fit(train_set, train_labels)
            model_train_score = model.score(train_set, train_labels)
            train_score.append(model_train_score)
            model_test_score = model.score(test_set, test_labels)
            test_score.append(model_test_score)

            self.models[tag] = model

            month_for_prediction = self.get_month_for_prediction(last_month)
            month_for_prediction = regular.transform(month_for_prediction)
            prediction = model.predict(month_for_prediction)
            prediction_for_three_month[tag] = list(prediction)

        #print(prediction_for_three_month)
        return prediction_for_three_month


    def get_month_for_prediction(self, first_month):
        result = pd.DataFrame([first_month, (first_month + 1)%13, (first_month + 2)%13], columns =['MONTH'])
        return result

    def create_dict_to_all_history(self):
        self.calculate_prices()
        data_dict = self.data.to_dict('split')
        return data_dict

    def save_data_to_excel(self):
        self.data.to_excel(self.file_save_path, engine='xlsxwriter', float_format="%.3f")

    def create_dict_for_stats(self):
        self.calculate_prices()
        # Dictionary for the first table
        columns_name = ['Cold Water', 'Hot Water', 'Total']
        rows_name = ['Average value per year', 'Average cost per year', 'Average value', 'Average cost']

        current_year = datetime.date.today()
        current_year = int(current_year.year)
        data_aver_value_per_year = [self.data[self.data['YEAR'] == current_year]['DELTA_CVS'].mean(), self.data[self.data['YEAR'] == current_year]['DELTA_HVS'].mean(), self.data[self.data['YEAR'] == current_year]['DELTA_CVS'].mean() + self.data[self.data['YEAR'] == current_year]['DELTA_HVS'].mean()]
        data_aver_cost_per_year = [self.data[self.data['YEAR'] == current_year]['PRICE_CVS'].mean(), self.data[self.data['YEAR'] == current_year]['PRICE_HVS'].mean(), self.data[self.data['YEAR'] == current_year]['TOTAL'].mean()]
        data_aver_value = [self.data['DELTA_CVS'].mean(), self.data['DELTA_HVS'].mean(), self.data['DELTA_CVS'].mean()+self.data['DELTA_HVS'].mean()]
        data_aver_cost = [self.data['PRICE_CVS'].mean(), self.data['PRICE_HVS'].mean(), self.data['TOTAL'].mean()]

        dict_for_first_stats = {'columns': columns_name, 'rows': rows_name, 'data': [data_aver_value_per_year, data_aver_cost_per_year, data_aver_value, data_aver_cost]}
        
        # Dictionary for the second table
        years_rows_name = ['Average value per year', 'Average cost per year']
        years_columns_name = []
        years_values_for_data = {'cold': [], 'hot': [], 'total': []}
        years_cost_for_data = {'cold': [], 'hot': [], 'total': []}
        first_year = self.data['YEAR'].min()
        while first_year<= current_year:
            years_columns_name.append(str(first_year))
            years_values_for_data['cold'].append(self.data[self.data['YEAR'] == first_year]['DELTA_CVS'].mean())
            years_values_for_data['hot'].append(self.data[self.data['YEAR'] == first_year]['DELTA_HVS'].mean())
            years_values_for_data['total'].append(self.data[self.data['YEAR'] == first_year]['DELTA_CVS'].mean() + self.data[self.data['YEAR'] == first_year]['DELTA_HVS'].mean())
            years_cost_for_data['cold'].append(self.data[self.data['YEAR'] == first_year]['PRICE_CVS'].mean())
            years_cost_for_data['hot'].append(self.data[self.data['YEAR'] == first_year]['PRICE_HVS'].mean())
            years_cost_for_data['total'].append(self.data[self.data['YEAR'] == first_year]['TOTAL'].mean())
            first_year += 1

        
        dict_for_years_cold_water_stats = {'columns': years_columns_name, 'rows': years_rows_name, 'data': [years_values_for_data['cold'], years_cost_for_data['cold']]}
        dict_for_years_hot_water_stats = {'columns': years_columns_name, 'rows': years_rows_name, 'data': [years_values_for_data['hot'], years_cost_for_data['hot']]}
        dict_for_years_total_water_stats = {'columns': years_columns_name, 'rows': years_rows_name, 'data': [years_values_for_data['total'], years_cost_for_data['total']]}
        dict_for_years_stats = {'cold': dict_for_years_cold_water_stats, 'hot': dict_for_years_hot_water_stats, 'total': dict_for_years_total_water_stats}
        #print(dict_for_first_stats, dict_for_years_stats)

        # Dictionary per month
        month_rows_name = ['Cold Water', 'Hot Water', 'Total']
        month_columns_name = self.month_list
        cold_month_value_for_data = []
        hot_month_value_for_data = []
        total_month_value_for_data = []
        cold_month_cost_for_data = []
        hot_month_cost_for_data = []
        total_month_cost_for_data = []
        for month in self.month_list:
            cold_month_value_for_data.append(self.data[self.data['MONTH'] == month]['DELTA_CVS'].mean())
            hot_month_value_for_data.append(self.data[self.data['MONTH'] == month]['DELTA_HVS'].mean())
            total_month_value_for_data.append(self.data[self.data['MONTH'] == month]['DELTA_CVS'].mean() + self.data[self.data['MONTH'] == month]['DELTA_HVS'].mean())
            cold_month_cost_for_data.append(self.data[self.data['MONTH'] == month]['PRICE_CVS'].mean())
            hot_month_cost_for_data.append(self.data[self.data['MONTH'] == month]['PRICE_HVS'].mean())
            total_month_cost_for_data.append(self.data[self.data['MONTH'] == month]['TOTAL'].mean())

        dict_for_month_value_stats = {'columns': month_columns_name, 'rows': month_rows_name, 'data': [cold_month_value_for_data, hot_month_value_for_data, total_month_value_for_data]}
        dict_for_month_cost_stats = {'columns': month_columns_name, 'rows': month_rows_name, 'data': [cold_month_cost_for_data, hot_month_cost_for_data, total_month_cost_for_data]}

        
        return dict_for_first_stats, dict_for_years_stats, dict_for_month_value_stats, dict_for_month_cost_stats

    def create_graphs_for_stats(self):
        # Average per month
        dict_for_first_stats, dict_for_years_stats, dict_for_month_value_stats, dict_for_month_cost_stats = self.create_dict_for_stats()
        self.create_average_per_month_graph(dict_for_month_cost_stats['data'][0], 'Cold Water Cost, rub', '#34495E')
        self.create_average_per_month_graph(dict_for_month_cost_stats['data'][1], 'Hot Water Cost, rub', '#34495E')
        self.create_average_per_month_graph(dict_for_month_cost_stats['data'][2], 'Water Cost, rub')

    def create_average_per_month_graph(self, y_data, y_axis_label, bar_color = '#2471A3'):
        colors = [bar_color] * len(self.month_list)
        x_ticks = [i for i in range(len(self.month_list))]
        x_labels = map(lambda x: self.month_mapping_shorter_dict[x], self.month_list)
        fig = plt.figure(figsize = (10, 5), tight_layout = True)
        ax = fig.add_subplot()
        width = 0.9
        ax.bar(x_ticks, y_data, width, color = colors)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels, size=20)
        ax.set_xlabel('Month', size=25)
        ax.set_ylabel(y_axis_label, size=25)
        ax.tick_params(axis='y', labelsize=20)
        #plt.savefig(f'temp/{tag}.png')
        plt.show()





myData = DataProcessing()
myData.create_graphs_for_stats()
#myData.delete_last_line_in_file()
#myData.create_graphs_to_new_value_analysis()
#myData.calculate_prices()
#myData.create_dict_to_all_history()
