def eksik_alan_kontrol(veri,gerekli_alanlar):
    for alan in gerekli_alanlar:
        if not veri.get(alan):
            return alan
    return None

def tip_kontrol(veri):
    if "yil" in veri and not isinstance(veri["yil"],(int)):
        return "yil"
    return None
