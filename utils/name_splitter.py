def split_name(url):
    part_name = url.split('/')
    return  '_'.join([part_name[-2], part_name[-1]])