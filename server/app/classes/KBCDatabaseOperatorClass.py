
from orator import DatabaseManager, Schema

from KBCMySQLConfigureClass import KBCMySQLConfigureClass


class KBCDatabaseOperatorClass(KBCMySQLConfigureClass):
    '''
    TODO:
    Creating MySQL table
    '''


    def __init__(self, database):

        # initializing the configuration
        super(self.__class__, self).__init__()

        self.config['mysql']['database'] = database
        db = DatabaseManager(self.config)

        # define the orator schema builder
        self.schema     = Schema(db)
        self.db         = db
        self.database   = database



    def create_table(self, table_name, df_data, string_size=100, is_sequence=False):

        if len(df_data) < 1:
            return False

        columns_list = df_data.columns.values

        self.schema.drop_if_exists(table_name)
        with self.schema.create(table_name) as table:

            # Creating new table based on the number of column and type of column.
            for column_name in columns_list:

                cell_value = df_data[column_name][0]

                if is_sequence is True and column_name=='Sequence':
                    table.text(column_name)

                elif isinstance(cell_value, int):
                    table.integer(column_name)

                elif isinstance(cell_value, float):
                    table.double(column_name, 15, 8)

                elif isinstance(cell_value, str):
                    table.string(column_name, string_size)

    def update_table_condition_two(self, table_name, condition_name1, value1, condition_name2, value2, dict_data):
        self.db.table(table_name).where(condition_name1, value1).where(condition_name2, value2).update(dict_data)


    def insert_table(self, table_name, df_data={}, dict_data={}):

        if len(df_data)<1 and len(dict_data)<1:
            return False

        if len(df_data)>0:
            # Changing pandas data frame to dictionary type
            df_data_dict = df_data.to_dict(orient='records')
        else:
            df_data_dict = dict_data;

        if self.schema.has_table(table_name):
            print(table_name)
            self.db.table(table_name).insert( df_data_dict )
        else:
            return False

    def naming_table(self, organism, data_type, version=''):
        if version == '':
            return organism + '_' + data_type
        else:
            return organism + '_' + data_type + '_' + version

    def pipeline(self, job_dict, organism, version='', string_size=100, no_version_table_list=[], sequence_table_list=[]):

        for data_type in job_dict:

            df_data = job_dict[data_type]
            if data_type not in no_version_table_list:
                table_name = self.naming_table(organism, data_type, version)
            else:
                table_name = self.naming_table(organism, data_type)

            if data_type in sequence_table_list:
                self.create_table(table_name, df_data, is_sequence=True)
            else:
                self.create_table(table_name, df_data, string_size)

            # Inerting data into database
            self.insert_table(table_name, df_data=df_data)

    def test(self):
        print("DB:" + self.db)
        print("test")
