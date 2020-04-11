
def calculate_estimate(data, factor=512, level='impact'):
    res = {}
    if level == 'impact':
        res['currentlyInfected'] = data['reportedCases'] * 10
        res['infectionsByRequestedTime'] = res['currentlyInfected'] * factor
    elif level == 'severImpact':
        res['currentlyInfected'] = data['reportedCases'] * 50
        res['infectionsByRequestedTime'] = res['currentlyInfected'] * factor

    available_beds = round(0.35 * data['totalHospitalBeds'])
    res['severeCasesByRequestedTime'] = 0.15 * res['infectionsByRequestedTime']
    res['hospitalBedsByRequestedTime'] = available_beds - res['severeCasesByRequestedTime']
    return res


def estimator(data):
    # convert time
    converted_time = data['timeToElapse']
    if data['periodType'] == 'weeks':
        converted_time = converted_time * 7
    elif data['periodType'] == 'months':
        converted_time = converted_time * 30
    # calculate factor value
    factor = 2 ** (converted_time // 3)
    impact = calculate_estimate(data, factor=factor)
    severe_impact = calculate_estimate(
        data, factor=factor, level='severImpact')
    result = {
        'data': data,
        'impact': impact,
        'severeImpact': severe_impact
    }
    return result
