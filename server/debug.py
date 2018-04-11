import app.CreateNewOrganism.EssentialDataMain as EssentialDataMain


if __name__ == '__main__':

    data = {'annotation':'/var/www/html/Dev/shuai/KBCommons_multi/storage/app/public/organism/medicago_truncatula_Mt4_0v1/Mtruncatula_285_Mt4.0v1.annotation'}
    data['version'] = 'v1'
    data['organism'] = 'Medtr'

    EssentialDataMain.main(data)