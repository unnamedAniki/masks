import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import random

from apps.model.settings import model_settings

products = {
    'ПК': 'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался классическим потребительским кредитом под маленькие проценты. Напиши лучшие рекламное предложение.',
    'TOPUP':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался рефинансированием внутреннего потребительский кредит в Газпромбанке. Напиши лучшие рекламное предложение.',
    'REFIN': 'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался рефинансированием  внешнего потребительский кредит в другом банке. Напиши лучшие рекламное предложение.',
    'CC':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент приобрел Кредитную карту \'Мир\'Газпромбанка. Напиши лучшие рекламное предложение, расскажи о вcех ее плюсах и почему ее надо заказать.',
    'AUTO': 'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Классическим автокредитом на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'AUTO_SCR': 'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался кредитом под залог автомобиля на лучших условиях. Напиши рекламное предложение, расскажи о всех его плюсах.',
    'MORTG':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Ипотекой на квартиру на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'MORTG_REFIN': 'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался рефинансированием ипотеки на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'MORTG_SCR':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Кредитом под залог недвижимости на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'MORTG_EA':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался ипотекой с доп. условиями на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'DEPOSIT':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Депозитом лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'SAVE_ACC':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Накопительным счетом на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'DC':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался дебетовой картой на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'PREMIUM':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался премиальной картой на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'INVEST':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался брокерским и инвестиционным счетом на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'ISG':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Инвестиционным страхованием жизни на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'NSG': 'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Накопительным страхование жизни на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'INS_LIFE':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался страхованием жизни на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'INS_PROPERTY':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Страхование имущества на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'TRUST':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Доверительным управлением счета на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'OMS':  'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Обезличенным металлический счетом на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
    'IZP': 'Напиши рекламный текст от лица Газпромбанка, чтобы клиент воспользовался Индивидуальным зарплатным проектом на лучших условиях. Напиши лучшие рекламное предложение, расскажи о всех его плюсах.',
}

columns = ['cnt_tr_all_3m', 'cnt_tr_top_up_3m', 'cnt_tr_cash_3m', 'cnt_tr_buy_3m', 'cnt_tr_mobile_3m',
           'cnt_tr_oil_3m', 'cnt_tr_on_card_3m', 'cnt_tr_service_3m', 'cnt_zp_12m', 'sum_zp_12m',
           'max_outstanding_amount_6m', 'avg_outstanding_amount_3m', 'cnt_dep_act', 'sum_dep_now',
           'avg_dep_avg_balance_1month', 'max_dep_avg_balance_3month', 'app_position_type_nm', 'visit_purposes',
           'app_vehicle_ind', 'qnt_months_from_last_visit', 'limit_exchange_count']

class Cluster:
    def __init__(self):
        self.path_data = model_settings.PATH_DATA
        self.path_cluster = model_settings.PATH_CLUSTER
        self.usersData = self.preprocessData()
        self.predictData = self.predictClust()
        self.average_max_dep = self.usersData['max_dep_avg_balance_3month'].mean()
        self.average_cnt_tr = self.usersData['cnt_tr_all_3m'].mean()
        self.average_cnt_tr_top = self.usersData['cnt_tr_top_up_3m'].mean()
        self.average_cnt_tr_cash = self.usersData['cnt_tr_cash_3m'].mean()
        self.average_cnt_tr_buy = self.usersData['cnt_tr_buy_3m'].mean()
        self.average_cnt_tr_mobile = self.usersData['cnt_tr_mobile_3m'].mean()
        self.average_cnt_tr_oil = self.usersData['cnt_tr_oil_3m'].mean()
        self.average_cnt_tr_card = self.usersData['cnt_tr_on_card_3m'].mean()
        self.average_cnt_tr_service = self.usersData['cnt_tr_service_3m'].mean()
        self.average_cnt_zp = self.usersData['cnt_zp_12m'].mean()
        self.criteria = {
            'TMO': ((self.usersData['age'] > 30) & (self.usersData['age'] < 70) & (self.usersData['cnt_tr_all_3m'] > 10)),
            'SMS': ((self.usersData['age'] > 20) & (self.usersData['age'] < 55) & (self.usersData['sum_zp_12m'] > 100000)),
            'PUSH': ((self.usersData['age'] > 20) & (self.usersData['age'] < 55) & (
                        self.usersData['max_outstanding_amount_6m'] == 0)),
            'EMAIL': ((self.usersData['age'] > 30) & (self.usersData['age'] < 55) & (self.usersData['app_vehicle_ind'] == 1)),
            'MOB_BANNER': ((self.usersData['age'] > 20) & (self.usersData['age'] < 30) & (
                    self.usersData['qnt_months_from_last_visit'] < 3)),
            'OFFICE_BANNER': ((self.usersData['age'] > 20) & (self.usersData['age'] < 70) & (
                    self.usersData['qnt_months_from_last_visit'] < 4)),
            'MOBILE_CHAT': (
                        (self.usersData['age'] > 20) & (self.usersData['age'] < 30) & (self.usersData['cnt_tr_service_3m'] > 0)),
            'KND': ((self.usersData['age'] > 20) & (self.usersData['age'] < 30) & (self.usersData['cnt_tr_buy_3m'] > 0)),
        }

    def importModel(self):
        loaded_model = joblib.load(self.path_cluster)
        return loaded_model

    def predictClust(self):
        model = self.importModel()
        print(model)
        predict = model.predict(self.usersData)
        return predict

    def preprocessData(self) -> pd.DataFrame:
        usersData = pd.read_excel(self.path_data)
        label_encoder = LabelEncoder()

        usersData['reg_region_nm'] = label_encoder.fit_transform(usersData['reg_region_nm'])
        usersData['visit_purposes'] = label_encoder.fit_transform(usersData['visit_purposes'])
        usersData['app_position_type_nm'] = label_encoder.fit_transform(usersData['app_position_type_nm'])

        usersData['gender'].fillna(-1, inplace=True)

        for column in columns:
            mean_value = usersData[column].mean()
            usersData[column].fillna(mean_value, inplace=True)

        return usersData

    def generateChannel(self):
        channel_assignments = {channel: self.usersData[self.criteria[channel]].index.tolist() for channel in self.criteria}
        return channel_assignments


    def generatePrompt(self):
        recommendations = {}
        for index, row in self.usersData.iterrows():
            client_age = row['age']
            client_region = row['reg_region_nm']

            for product, criteria in products.items():

                product_append = []
                if (product == 'PREMIUM' and (
                        row['app_position_type_nm'] == 'руководитель (зам. рук-ля) подразделения' or row[
                    'app_position_type_nm'] == 'руководитель (зам. рук-ля) организации')):
                    product_append.append(product)

                if (product == 'OMS' and (
                        row['app_position_type_nm'] == 'руководитель (зам. рук-ля) подразделения' or row[
                    'app_position_type_nm'] == 'руководитель (зам. рук-ля) организации')):
                    product_append.append(product)

                if (product == 'IZP' and (
                        row['app_position_type_nm'] == 'руководитель (зам. рук-ля) подразделения' or row[
                    'app_position_type_nm'] == 'руководитель (зам. рук-ля) организации')):
                    product_append.append(product)

                if (product == 'ISG' and (
                        row['app_position_type_nm'] == 'руководитель (зам. рук-ля) подразделения' or row[
                    'app_position_type_nm'] == 'руководитель (зам. рук-ля) организации')):
                    product_append.append(product)

                if (product == 'TOPUP' and (
                        row['max_outstanding_amount_6m'] > 0 or row['avg_outstanding_amount_3m'] > 0)):
                    product_append.append(product)

                if (product == 'REFIN' and (
                        row['max_outstanding_amount_6m'] > 0 or row['avg_outstanding_amount_3m'] > 0)):
                    product_append.append(product)

                if (product == 'MORTG_EA' and row['reg_region_nm'] in ['Якутия', 'Бурятия', 'Забайкальский край',
                                                                       'Приморский край', 'Камчатский край',
                                                                       'Хабаровский край', 'Магаданская область',
                                                                       'Амурская область', 'Сахалинская область',
                                                                       'Еврейская автономная область',
                                                                       'Чукотский автономный округ'] and 20 <= client_age <= 36 and pd.isna(
                    row['max_outstanding_amount_6m']) and pd.isna(row['avg_outstanding_amount_3m'])):
                    product_append.append(product)
                    # print(index, row)
                    # recommendations.setdefault(index, []).append(product)

                if (product == 'MORTG_REFIN' and row['age'] > 30 and (
                        row['max_outstanding_amount_6m'] > 0 or row['avg_outstanding_amount_3m'] > 0)):
                    product_append.append(product)

                if (product == 'AUTO_SCR' and row['app_vehicle_ind'] == 1):
                    product_append.append(product)

                if (product == 'AUTO' and row['app_vehicle_ind'] == 0 and row['cnt_tr_oil_3m'] > 0):
                    product_append.append(product)

                if (product == 'DEPOSIT' and (row['cnt_dep_act'] >= 1 or row['visit_purposes'] == "DEPOSIT")):
                    product_append.append(product)

                if (product == 'SAVE_ACC' and row['avg_dep_avg_balance_1month'] > 0):
                    product_append.append(product)

                if (product == 'TRUST' and row['max_dep_avg_balance_3month'] > self.average_max_dep):
                    product_append.append(product)

                if (product == 'ПК' and ((row['cnt_tr_all_3m'] > self.average_cnt_tr / 2 and row['age']) or row[
                    "visit_purposes"] == "POTREB")):
                    product_append.append(product)
                if (product == 'СС' and row['cnt_tr_all_3m'] > self.average_cnt_tr / 2):
                    product_append.append(product)

                if (product == 'INS_LIFE' and (row['app_position_type_nm'] == 'Военнослужащий')):
                    product_append.append(product)
                if (product == 'NSG' and (row['app_position_type_nm'] == 'Военнослужащий')):
                    product_append.append(product)

                if (product == 'DC' and ((row['cnt_tr_all_3m'] > self.average_cnt_tr / 2 or row[
                    'cnt_tr_top_up_3m'] > self.average_cnt_tr_top / 2 or row['cnt_tr_cash_3m'] > self.average_cnt_tr_cash / 2) or
                                         row['visit_purposes'] == "DCARD")):
                    product_append.append(product)

                if (product == 'CC' and (((row['cnt_tr_all_3m'] > self.average_cnt_tr / 2 or row[
                    'cnt_tr_top_up_3m'] > self.average_cnt_tr_top / 2 or row['cnt_tr_cash_3m'] > self.average_cnt_tr_cash / 2) and
                                          row['age'] > 30) or row['visit_purposes'] == "CCARD")):
                    product_append.append(product)
                if (product == 'MORTG_SCR' and (((row['cnt_tr_all_3m'] > self.average_cnt_tr / 2 or row[
                    'cnt_tr_top_up_3m'] > self.average_cnt_tr_top / 2 or row['cnt_tr_cash_3m'] > self.average_cnt_tr_cash / 2) and
                                                 row['age'] > 30) or row['visit_purposes'] == "CCARD")):
                    product_append.append(product)

                if (product == 'INVEST' and row['visit_purposes'] == "INVEST"):
                    product_append.append(product)

                if (product == 'ISG' and row['visit_purposes'] == "INVEST" and row['age'] > 30):
                    product_append.append(product)
                if (product == 'NSG' and row['visit_purposes'] == "DEPOSIT" and row['age'] > 30):
                    product_append.append(product)
                if (product == 'INS_LIFE' and row['visit_purposes'] == "CREDIT" and row['age'] > 35):
                    product_append.append(product)
                if (product == 'INS_PROPERTY' and (
                        row['visit_purposes'] == "DEPOSIT" or row['visit_purposes'] == "INVEST" or row[
                    'visit_purposes'] == "CREDIT") and row['age'] > 35):
                    product_append.append(product)

                if (product == 'CURR_EXC' and row['visit_purposes'] == "PAY" and row['age'] > 30):
                    product_append.append(product)

                unique_elements = set(product_append)

                result_array = list(unique_elements)

                if len(product_append) > 0:
                    for i in result_array:
                        recommendations.setdefault(index, []).append(i)

        return recommendations

    def recommend_product(self, predict):
        recommendations = {}
        predict = self.predictClust()
        for index, prediction in enumerate(predict):
            if prediction == 0:
                recommendations[index] = products[('PREMIUM')]

            elif prediction == 1:
                recommendations[index] = products[('TOPUP')]

            elif prediction == 2:
                recommendations[index] = products[('ПК')]

            elif prediction == 3:
                recommendations[index] = products[('DC')]

            elif prediction == 4:
                recommendations[index] = products[('TRUST')]

            elif prediction == 5:
                recommendations[index] = products[('DEPOSIT')]

            elif prediction == 6:
                recommendations[index] = products[('AUTO')]

            elif prediction == 7:
                recommendations[index] = products[('IZP')]

            elif prediction == 8:
                recommendations[index] = products[('MORTG_REFIN')]

            elif prediction == 9:
                recommendations[index] = products[('DEPOSIT')]

            elif prediction == 10:
                recommendations[index] = products[('DC')]

        return recommendations



