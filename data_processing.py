import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import datetime
import os

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
        self.path_to_graph_folder_stats = 'temp/graph_for_stats'
        self.path_to_graph_folder_new_month = 'temp/graph_for_month'
        self.path_to_graph_folder_pred = 'temp/graph_for_pred'
        
        self.cold_water_price = c.cold_water_price
        self.hot_water_price = c.hot_water_price
        self.month_number_to_plot = c.month_number_to_plot
        self.last_cvs_value = 0
        self.last_hvs_value = 0
        self.prediction_for_three_month = {'cold': None, 'hot': None}
        self.last_month = None

        self.current_year = datetime.date.today()
        self.current_year = int(self.current_year.year)

        self.month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
        'August', 'September', 'October', 'November', 'December']
        self.month_mapping_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 
        'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        self.month_mapping_reverce_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 
        8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        self.month_mapping_shorter_dict = {'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr', 'May':'May', 'June': 'Jun', 'July': 'Jul', 
        'August': 'Aug', 'September':'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec'}

        self.data_loader()

    # Load data from file to pandas df
    def data_loader(self):
        self.data = pd.read_csv(self.data_path, sep = '\t', header=0)

        if len(self.data) < self.month_number_to_plot:
            self.month_number_to_plot = len(self.data)

        self.last_cvs_value = self.data['CVS'].loc[len(self.data)-1]
        self.last_hvs_value = self.data['HVS'].loc[len(self.data)-1]  

    # Add new values to the and of the data file
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

    # Calculate deltas and prices
    def calculate_prices(self):
        self.data['DELTA_CVS'] = 0.00
        self.data['DELTA_HVS'] = 0.00
        self.data['PRICE_CVS'] = 0.00
        self.data['PRICE_HVS'] = 0.00
        self.data['TOTAL'] = 0.00
        self.data['TOTAL_DELTA'] = 0.00
        for i in range(1, len(self.data)):
            self.data['DELTA_CVS'].loc[i] = self.data['CVS'].loc[i] - self.data['CVS'].loc[i-1]
            self.data['DELTA_HVS'].loc[i] = self.data['HVS'].loc[i] - self.data['HVS'].loc[i-1]
            self.data['PRICE_CVS'].loc[i] = self.data['DELTA_CVS'].loc[i] * self.cold_water_price
            self.data['PRICE_HVS'].loc[i] = self.data['DELTA_HVS'].loc[i] * self.hot_water_price
            self.data['TOTAL'].loc[i] = self.data['PRICE_CVS'].loc[i] + self.data['PRICE_HVS'].loc[i]
            self.data['TOTAL_DELTA'].loc[i] = self.data['DELTA_CVS'].loc[i] + self.data['DELTA_HVS'].loc[i]

    # Create dictionary with values to the new data analysis widget
    def data_to_new_value_analysis(self):
        self.calculate_prices()
        self.make_model_for_prediction()

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
        'price_cvs_pred': self.prediction_for_three_month['cold'][0]*self.cold_water_price,
        'price_hvs_pred': self.prediction_for_three_month['hot'][0]*self.hot_water_price,
        'total_delta': self.data['TOTAL_DELTA'].loc[i],
        'total_delta_aver': self.data['TOTAL_DELTA'].loc[:i].mean()}

        #self.create_graphs_to_new_value_analysis()
        return result_dict

    # Create graphs to the new data analysis widget
    def create_graphs_to_new_value_analysis(self):
        #self.data_to_new_value_analysis()

        # Check directory for graphs saving
        if not os.path.exists(self.path_to_graph_folder_new_month):
            os.mkdir(self.path_to_graph_folder_new_month)

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
            plt.savefig(f'{self.path_to_graph_folder_new_month}/{tag}.png')
            plt.close('all')
            #plt.show()

    # Delete last values in the data file and update dataframe
    def delete_last_line_in_file(self):
        with open(self.data_path, 'r') as f:
            lines = f.readlines()
            lines = lines[:-1]

        with open(self.data_path, 'w') as f:
            f.writelines(lines)

        self.data_loader()

    # Create model to predict deltas (KNRegression)
    def make_model_for_prediction(self):
        self.calculate_prices()

        self.data['MONTH_MAPPED'] = self.data['MONTH'].map(self.month_mapping_dict)
        self.last_month = self.data['MONTH_MAPPED'].loc[len(self.data)-1]

        features = self.data[['MONTH_MAPPED']].iloc[1:]
        deltas = {'cold': self.data['DELTA_CVS'].iloc[1:], 'hot': self.data['DELTA_HVS'].iloc[1:]}
        #prediction_for_three_month = {'cold': None, 'hot': None}
        self.models = {'cold': None, 'hot': None}

        for tag, delta in deltas.items():
            # Perform train, test, split
            train_set, test_set, train_labels, test_labels = train_test_split(features, delta, test_size = 0.2, random_state = 100)
            # Scale the feature data so it has mean = 0 and standard deviation = 1
            regular = StandardScaler()
            train_set = regular.fit_transform(train_set)
            test_set = regular.transform(test_set)
            # Create and train the models
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

            month_for_prediction = self.get_month_for_prediction(self.last_month)
            month_for_prediction = regular.transform(month_for_prediction)
            prediction = model.predict(month_for_prediction)
            self.prediction_for_three_month[tag] = list(prediction)


    # Create month dataframe for prediction
    def get_month_for_prediction(self, first_month):
        result = pd.DataFrame([first_month, (first_month + 1)%13, (first_month + 2)%13, (first_month + 3)%13], columns =['MONTH'])
        return result

    # Create dictionary and graphs for prediction widget
    def create_content_for_prediction(self):
        # Check directory for plot picture saving
        if not os.path.exists(self.path_to_graph_folder_pred):
            os.mkdir(self.path_to_graph_folder_pred)

        # Make prediction
        self.make_model_for_prediction()

        # Prepair data to current year + prediction month plots
        df_to_plot = self.data[self.data['YEAR'] == self.current_year][['MONTH', 'PRICE_CVS', 'PRICE_HVS']].reset_index(drop=True)
        predicted_month = [self.last_month, (self.last_month + 1)%13, (self.last_month + 2)%13, (self.last_month + 3)%13]
        predicted_month = map(lambda x: self.month_mapping_reverce_dict[x], predicted_month)
        predicted_month = list(predicted_month)
        current_year_month = list(df_to_plot['MONTH'])
        current_year_month.extend(predicted_month[1:])

        predicted_cold_data = list(self.prediction_for_three_month['cold'])
        predicted_cold_data = [value*self.cold_water_price for value in predicted_cold_data]
        cold_data = list(df_to_plot['PRICE_CVS'])
        cold_data.extend(predicted_cold_data[1:])
        self.create_values_per_current_year_bar(current_year_month, cold_data, self.path_to_graph_folder_pred, 'Cold Water Cost, rub', 'cold_cost', '#AF7AC5', 3, '#F4D03F')

        predicted_hot_data = list(self.prediction_for_three_month['hot'])
        predicted_hot_data = [value*self.hot_water_price for value in predicted_hot_data]
        hot_data = list(df_to_plot['PRICE_HVS'])
        hot_data.extend(predicted_hot_data[1:])
        self.create_values_per_current_year_bar(current_year_month, hot_data, self.path_to_graph_folder_pred, 'Hot Water Cost, rub', 'hot_cost', '#884EA0', 3, '#D4AC0D')

        total_data = [hot_data[i] + cold_data[i] for i in range(len(cold_data))]
        self.create_values_per_current_year_bar(current_year_month, total_data, self.path_to_graph_folder_pred, 'Water Cost, rub', 'total_cost', '#D7BDE2', 3, '#F9E79F')
        
        # Create data dictionary
        dict_for_table = {'cold': cold_data[-3:], 'hot': hot_data[-3:], 'total': total_data[-3:], 'month': predicted_month[1:]}
        return dict_for_table

    # Create dictionary from dataframe to history widget
    def create_dict_to_all_history(self):
        self.calculate_prices()
        data_dict = self.data.to_dict('split')
        return data_dict

    def save_data_to_excel(self):
        self.data.to_excel(f"{self.file_save_path}/history.xlsx", engine='xlsxwriter', float_format="%.3f")

    # Update some const values and pathes
    def update_const(self, new_values_list):
        self.data_path = new_values_list[1]
        self.file_save_path = new_values_list[0]
        self.cold_water_price = new_values_list[2]
        self.hot_water_price = new_values_list[3]
        self.month_number_to_plot = new_values_list[4]
        self.data_loader()

    # Create dictionaries for stats widget
    def create_dict_for_stats(self):
        """
        Method returns four dictionaries:

        - First dict with: average delta and cost for current year, average delta and cost (for all data)
        - Second dict with: average deltas and costs for every year
        - Third dict with: average deltas for every month for the current year
        - Fourth dict with: average costs for every month for the current year

        """
        self.calculate_prices()

        # Dictionary for the first table
        columns_name = ['Cold Water', 'Hot Water', 'Total']
        rows_name = ['Average value per year', 'Average cost per year', 'Average value', 'Average cost']

        data_aver_value_per_year = [self.data[self.data['YEAR'] == self.current_year]['DELTA_CVS'].mean(), self.data[self.data['YEAR'] == self.current_year]['DELTA_HVS'].mean(), self.data[self.data['YEAR'] == self.current_year]['TOTAL_DELTA'].mean()]
        data_aver_cost_per_year = [self.data[self.data['YEAR'] == self.current_year]['PRICE_CVS'].mean(), self.data[self.data['YEAR'] == self.current_year]['PRICE_HVS'].mean(), self.data[self.data['YEAR'] == self.current_year]['TOTAL'].mean()]
        data_aver_value = [self.data['DELTA_CVS'].mean(), self.data['DELTA_HVS'].mean(), self.data['TOTAL_DELTA'].mean()]
        data_aver_cost = [self.data['PRICE_CVS'].mean(), self.data['PRICE_HVS'].mean(), self.data['TOTAL'].mean()]

        dict_for_first_stats = {'columns': columns_name, 'rows': rows_name, 'data': [data_aver_value_per_year, data_aver_cost_per_year, data_aver_value, data_aver_cost]}
        
        # Dictionary for the second table
        years_rows_name = ['Average value per year', 'Average cost per year']
        years_columns_name = [] #years from the first to the current year
        years_values_for_data = {'cold': [], 'hot': [], 'total': []}
        years_cost_for_data = {'cold': [], 'hot': [], 'total': []}
        first_year = self.data['YEAR'].min()
        while first_year<= self.current_year:
            years_columns_name.append(str(first_year))
            years_values_for_data['cold'].append(self.data[self.data['YEAR'] == first_year]['DELTA_CVS'].mean())
            years_values_for_data['hot'].append(self.data[self.data['YEAR'] == first_year]['DELTA_HVS'].mean())
            years_values_for_data['total'].append(self.data[self.data['YEAR'] == first_year]['TOTAL_DELTA'].mean())
            years_cost_for_data['cold'].append(self.data[self.data['YEAR'] == first_year]['PRICE_CVS'].mean())
            years_cost_for_data['hot'].append(self.data[self.data['YEAR'] == first_year]['PRICE_HVS'].mean())
            years_cost_for_data['total'].append(self.data[self.data['YEAR'] == first_year]['TOTAL'].mean())
            first_year += 1

        dict_for_years_cold_water_stats = {'columns': years_columns_name, 'rows': years_rows_name, 'data': [years_values_for_data['cold'], years_cost_for_data['cold']]}
        dict_for_years_hot_water_stats = {'columns': years_columns_name, 'rows': years_rows_name, 'data': [years_values_for_data['hot'], years_cost_for_data['hot']]}
        dict_for_years_total_water_stats = {'columns': years_columns_name, 'rows': years_rows_name, 'data': [years_values_for_data['total'], years_cost_for_data['total']]}
        dict_for_years_stats = {'cold': dict_for_years_cold_water_stats, 'hot': dict_for_years_hot_water_stats, 'total': dict_for_years_total_water_stats}
        #print(dict_for_first_stats, dict_for_years_stats)

        # Dictionary for tables per month
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
            total_month_value_for_data.append(self.data[self.data['MONTH'] == month]['TOTAL_DELTA'].mean())
            cold_month_cost_for_data.append(self.data[self.data['MONTH'] == month]['PRICE_CVS'].mean())
            hot_month_cost_for_data.append(self.data[self.data['MONTH'] == month]['PRICE_HVS'].mean())
            total_month_cost_for_data.append(self.data[self.data['MONTH'] == month]['TOTAL'].mean())

        dict_for_month_value_stats = {'columns': month_columns_name, 'rows': month_rows_name, 'data': [cold_month_value_for_data, hot_month_value_for_data, total_month_value_for_data]}
        dict_for_month_cost_stats = {'columns': month_columns_name, 'rows': month_rows_name, 'data': [cold_month_cost_for_data, hot_month_cost_for_data, total_month_cost_for_data]}

        
        return dict_for_first_stats, dict_for_years_stats, dict_for_month_value_stats, dict_for_month_cost_stats

    # Create graphs for stats widget
    def create_graphs_for_stats(self):

        # Check directory for plot picture saving
        if not os.path.exists(self.path_to_graph_folder_stats):
            os.mkdir(self.path_to_graph_folder_stats)
        
        # Average values in dictionaries
        dict_for_first_stats, dict_for_years_stats, dict_for_month_value_stats, dict_for_month_cost_stats = self.create_dict_for_stats()
        
        # Create graphs (bar plot)
        self.create_average_per_month_bar(dict_for_month_cost_stats['data'][0], 'Cold Water Cost, rub', 'cold_cost', '#D6EAF8')
        self.create_average_per_month_bar(dict_for_month_cost_stats['data'][1], 'Hot Water Cost, rub', 'hot_cost', '#85C1E9')
        self.create_average_per_month_bar(dict_for_month_cost_stats['data'][2], 'Water Cost, rub', 'total_cost', '#2E86C1')

        self.create_average_per_month_bar(dict_for_month_value_stats['data'][0], 'Cold Water Value, m3 ', 'cold_value', '#D1F2EB')
        self.create_average_per_month_bar(dict_for_month_value_stats['data'][1], 'Hot Water Value, m3 ', 'hot_value', '#76D7C4')
        self.create_average_per_month_bar(dict_for_month_value_stats['data'][2], 'Water Value, m3 ', 'total_value', '#1ABC9C')

        self.create_average_per_years_bar(dict_for_years_stats['cold']['data'][1], 'Cold Water Cost, rub', 'cold_cost', '#F9E79F')
        self.create_average_per_years_bar(dict_for_years_stats['hot']['data'][1], 'Hot Water Cost, rub', 'hot_cost', '#F4D03F')
        self.create_average_per_years_bar(dict_for_years_stats['total']['data'][1], 'Water Cost, rub', 'total_cost', '#D4AC0D')

        self.create_average_per_years_bar(dict_for_years_stats['cold']['data'][0], 'Cold Water Value, m3 ', 'cold_value', '#AEB6BF')
        self.create_average_per_years_bar(dict_for_years_stats['hot']['data'][0], 'Hot Water Value, m3 ', 'hot_value', '#85929E')
        self.create_average_per_years_bar(dict_for_years_stats['total']['data'][0], 'Water Value, m3 ', 'total_value', '#34495E')

        # Prepair data to current year plots
        df_to_plot = self.data[self.data['YEAR'] == self.current_year][['MONTH', 'PRICE_CVS', 'PRICE_HVS', 'TOTAL']].reset_index(drop=True)
        current_year_month = list(df_to_plot['MONTH'])
        self.create_values_per_current_year_bar(current_year_month, list(df_to_plot['PRICE_CVS']), self.path_to_graph_folder_stats, 'Cold Water Cost, rub', 'cold_cost', '#D7BDE2')
        self.create_values_per_current_year_bar(current_year_month, list(df_to_plot['PRICE_HVS']), self.path_to_graph_folder_stats,'Hot Water Cost, rub', 'hot_cost', '#AF7AC5')
        self.create_values_per_current_year_bar(current_year_month, list(df_to_plot['TOTAL']), self.path_to_graph_folder_stats,'Water Cost, rub', 'total_cost', '#884EA0')


    def create_average_per_month_bar(self, y_data, y_axis_label, file_suf = 'cost', bar_color = '#2471A3'):
        """
        Save all graphs (.png) to self.path_to_graph_folder_stats folder.

        Method need:
        - y_data: y values
        - y_axis_label: label y axis and for the plot
        - file_suf (default 'cost'): string suffict to put into graph file
        - bar_color (default '#2471A3'): color for bar
        """
        colors = [bar_color] * len(self.month_list)
        x_ticks = [i for i in range(len(self.month_list))]
        x_labels = map(lambda x: self.month_mapping_shorter_dict[x], self.month_list)
        fig = plt.figure(figsize = (10, 5), tight_layout = True)
        ax = fig.add_subplot()
        width = 0.9
        ax.bar(x_ticks, y_data, width, color = colors)
        ax.set_title(f'{y_axis_label[:-5]} per month', size=25)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels, size=20)
        ax.set_xlabel('Month', size=25)
        ax.set_ylabel(y_axis_label, size=25)
        ax.tick_params(axis='y', labelsize=20)
        plt.savefig(f'{self.path_to_graph_folder_stats}/month_{file_suf}.png')
        plt.close('all')
        #plt.show()

    def create_average_per_years_bar(self, y_data, y_axis_label, file_suf = 'cost', bar_color = '#2471A3'):
        """
        Save all graphs (.png) to self.path_to_graph_folder_stats folder.

        Method need:
        - y_data: y values
        - y_axis_label: label y axis and for the plot
        - file_suf (default 'cost'): string suffict to put into graph file
        - bar_color (default '#2471A3'): color for bar
        """
        first_year = self.data['YEAR'].min()
        x_ticks = [year for year in range(first_year, self.current_year+1)]
        colors = [bar_color] * len(x_ticks)
        fig = plt.figure(figsize = (10, 5), tight_layout = True)
        ax = fig.add_subplot()
        width = 0.9
        ax.bar(x_ticks, y_data, width, color = colors)
        ax.set_title(f'{y_axis_label[:-5]} per year', size=25)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_ticks, size=20)
        ax.set_xlabel('Year', size=25)
        ax.set_ylabel(y_axis_label, size=25)
        ax.tick_params(axis='y', labelsize=20)
        plt.savefig(f'{self.path_to_graph_folder_stats}/year_{file_suf}.png')
        plt.close('all')
        #plt.show()

    def create_values_per_current_year_bar(self, x_labels_list, y_data, path_name, y_axis_label, file_suf = 'cost', bar_color = '#2471A3', color_dif = 0, dif_color = '#F5B041'):
        """
        Save all graphs (.png) to path_name folder.

        Method need:
        - x_labels_list: labels array for x axis
        - y_data: y values
        - path_name: string path to folder where graphs will be saved
        - y_axis_label: label y axis and for the plot
        - file_suf (default 'cost'): string suffict to put into graph file
        - bar_color (default '#2471A3'): color for bar
        - color_dif (default 0): int n number to color n-last bars to different color
        - dif_color (default '#F5B041'): different color for n-last bars
        """
        if color_dif == 0:
            colors = [bar_color] * len(x_labels_list)
        else:
            colors = [bar_color] * (len(x_labels_list)-color_dif)+[dif_color]*color_dif
        x_ticks = [i for i in range(len(x_labels_list))]
        x_labels = map(lambda x: self.month_mapping_shorter_dict[x], x_labels_list)
        fig = plt.figure(figsize = (10, 5), tight_layout = True)
        ax = fig.add_subplot()
        width = 0.9
        ax.bar(x_ticks, y_data, width, color = colors)
        ax.set_title(f'{y_axis_label[:-5]} per month', size=25)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels, size=20)
        ax.set_xlabel('Month', size=25)
        ax.set_ylabel(y_axis_label, size=25)
        ax.tick_params(axis='y', labelsize=20)
        plt.savefig(f'{path_name}/current_{file_suf}.png')
        plt.close('all')
        #plt.show()


#myData = DataProcessing()
#myData.create_content_for_prediction()
#myData.delete_last_line_in_file()
#myData.create_graphs_to_new_value_analysis()
#myData.calculate_prices()
#myData.create_dict_to_all_history()
