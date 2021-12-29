def show_progress_bar(single_mandate, mandates=45, tiles=100):
    percent = int(single_mandate * tiles / mandates)
    space = tiles - percent
    print('  LOADING:', '[' + '|' * percent + ' ' * space + ']', str(percent) + '%','MANDATE:', str(single_mandate), end='\r')
