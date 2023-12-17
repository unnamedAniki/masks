import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from apps.model.settings import model_settings

const_prompt = "Напиши рекламный текст от лица Газпромбанка, чтобы клиент "
products = {
    'ПК': 'воспользовался классическим потребительским кредитом под маленькие проценты.',
    'TOPUP':  'воспользовался рефинансированием внутреннего потребительский кредит в Газпромбанке.',
    'REFIN': 'воспользовался рефинансированием  внешнего потребительский кредит в другом банке.',
    'CC':  'приобрел Кредитную карту \'Мир\'Газпромбанка.',
    'AUTO': 'воспользовался Классическим автокредитом на лучших условиях.',
    'AUTO_SCR': 'воспользовался кредитом под залог автомобиля на лучших условиях.',
    'MORTG':  'воспользовался Ипотекой на квартиру на лучших условиях.',
    'MORTG_REFIN': 'воспользовался рефинансированием ипотеки на лучших условиях.',
    'MORTG_SCR':  'воспользовался Кредитом под залог недвижимости на лучших условиях.',
    'MORTG_EA':  'воспользовался ипотекой с доп. условиями на лучших условиях.',
    'DEPOSIT':  'воспользовался Депозитом лучших условиях.',
    'SAVE_ACC':  'воспользовался Накопительным счетом на лучших условиях.',
    'DC':  'воспользовался дебетовой картой на лучших условиях.',
    'PREMIUM':  'воспользовался премиальной картой на лучших условиях.',
    'INVEST':  'воспользовался брокерским и инвестиционным счетом на лучших условиях.',
    'ISG':  'воспользовался Инвестиционным страхованием жизни на лучших условиях.',
    'NSG': 'воспользовался Накопительным страхование жизни на лучших условиях.',
    'INS_LIFE':  'воспользовался страхованием жизни на лучших условиях.',
    'INS_PROPERTY':  'воспользовался Страхование имущества на лучших условиях.',
    'TRUST':  'воспользовался Доверительным управлением счета на лучших условиях.',
    'OMS':  'воспользовался Обезличенным металлический счетом на лучших условиях.',
    'IZP': 'воспользовался Индивидуальным зарплатным проектом на лучших условиях.',
}

columns = ['cnt_tr_all_3m', 'cnt_tr_top_up_3m', 'cnt_tr_cash_3m', 'cnt_tr_buy_3m', 'cnt_tr_mobile_3m',
           'cnt_tr_oil_3m', 'cnt_tr_on_card_3m', 'cnt_tr_service_3m', 'cnt_zp_12m', 'sum_zp_12m',
           'max_outstanding_amount_6m', 'avg_outstanding_amount_3m', 'cnt_dep_act', 'sum_dep_now',
           'avg_dep_avg_balance_1month', 'max_dep_avg_balance_3month',
           'app_vehicle_ind', 'qnt_months_from_last_visit', 'limit_exchange_count']


class Cluster:
    def __init__(self):
        self.average_max_dep = None
        self.average_max_dep = None
        self.average_cnt_tr = None
        self.average_cnt_tr_top = None
        self.average_cnt_tr_cash = None
        self.average_cnt_tr_buy = None
        self.average_cnt_tr_mobile = None
        self.average_cnt_tr_oil = None
        self.average_cnt_tr_card = None
        self.average_cnt_tr_service = None
        self.average_cnt_zp = None
        self.criteria = None
        self.users_data = None
        self.path_data = model_settings.PATH_DATA
        self.path_cluster = model_settings.PATH_CLUSTER
        self.import_model = joblib.load(self.path_cluster)

    def preprocess_data(self, data) -> pd.DataFrame:
        users_data = pd.read_json(data)
        label_encoder = LabelEncoder()
        users_data['super_clust'] = label_encoder.fit_transform(users_data['super_clust'])
        users_data['reg_region_nm'] = label_encoder.fit_transform(users_data['reg_region_nm'])
        users_data['visit_purposes'] = label_encoder.fit_transform(users_data['visit_purposes'])
        users_data['app_position_type_nm'] = label_encoder.fit_transform(users_data['app_position_type_nm'])
        users_data['age'].fillna(-1, inplace=True)
        users_data['gender'].fillna(-1, inplace=True)

        for column in columns:
            mean_value = users_data[column].mean()
            users_data[column].fillna(mean_value, inplace=True)

        self.average_max_dep = users_data['max_dep_avg_balance_3month'].mean()
        self.average_cnt_tr = users_data['cnt_tr_all_3m'].mean()
        self.average_cnt_tr_top = users_data['cnt_tr_top_up_3m'].mean()
        self.average_cnt_tr_cash = users_data['cnt_tr_cash_3m'].mean()
        self.average_cnt_tr_buy = users_data['cnt_tr_buy_3m'].mean()
        self.average_cnt_tr_mobile = users_data['cnt_tr_mobile_3m'].mean()
        self.average_cnt_tr_oil = users_data['cnt_tr_oil_3m'].mean()
        self.average_cnt_tr_card = users_data['cnt_tr_on_card_3m'].mean()
        self.average_cnt_tr_service = users_data['cnt_tr_service_3m'].mean()
        self.average_cnt_zp = users_data['cnt_zp_12m'].mean()
        self.criteria = {
            'TMO': ((users_data['age'] > 30) & (users_data['age'] < 70) & (
                        users_data['cnt_tr_all_3m'] > 10)),
            'SMS': ((users_data['age'] > 20) & (users_data['age'] < 55) & (
                        users_data['sum_zp_12m'] > 100000)),
            'PUSH': ((users_data['age'] > 20) & (users_data['age'] < 55) & (
                    users_data['max_outstanding_amount_6m'] == 0)),
            'EMAIL': ((users_data['age'] > 30) & (users_data['age'] < 55) & (
                        users_data['app_vehicle_ind'] == 1)),
            'MOB_BANNER': ((users_data['age'] > 20) & (users_data['age'] < 30) & (
                    users_data['qnt_months_from_last_visit'] < 3)),
            'OFFICE_BANNER': ((users_data['age'] > 20) & (users_data['age'] < 70) & (
                    users_data['qnt_months_from_last_visit'] < 4)),
            'MOBILE_CHAT': (
                    (users_data['age'] > 20) & (users_data['age'] < 30) & (
                        users_data['cnt_tr_service_3m'] > 0)),
            'KND': ((users_data['age'] > 20) & (users_data['age'] < 30) & (
                        users_data['cnt_tr_buy_3m'] > 0)),
        }
        return users_data

    def generateChannel(self):
        channel_assignments = {channel: self.users_data[self.criteria[channel]].index.tolist() for channel in self.criteria}
        return channel_assignments

    def generatePrompt(self, json_data):
        self.users_data = self.preprocess_data(data=json_data)
        recommendations = {}
        for index, row in self.users_data.iterrows():
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

                if (product == 'MORTG_EA' and client_region in ['Якутия', 'Бурятия', 'Забайкальский край',
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
                        recommendations.setdefault(index, []).append(products[i])

        return recommendations




