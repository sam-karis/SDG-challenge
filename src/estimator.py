
def calculate_estimate(data, converted_time, level='impact'):
    res = {}
    # calculate factor value
    factor = 2 ** (converted_time // 3)
    # challenge one
    if level == 'impact':
        res['currentlyInfected'] = int(data['reportedCases'] * 10)
        res['infectionsByRequestedTime'] = res['currentlyInfected'] * factor
    elif level == 'severImpact':
        res['currentlyInfected'] = int(data['reportedCases'] * 50)
        res['infectionsByRequestedTime'] = int(
            res['currentlyInfected'] * factor)
    # challenge two
    res['severeCasesByRequestedTime'] = int(
        0.15 * res['infectionsByRequestedTime'])
    available_beds = 0.35 * data['totalHospitalBeds']
    res['hospitalBedsByRequestedTime'] = int(
        available_beds - res['severeCasesByRequestedTime'])
    # challenge three
    res['casesForICUByRequestedTime'] = int(
        0.05 * res['infectionsByRequestedTime'])
    res['casesForVentilatorsByRequestedTime'] = int(
        0.02 * res['infectionsByRequestedTime'])
    dollars_in_flight = res['infectionsByRequestedTime'] * \
        data['region']['avgDailyIncomePopulation'] * \
        data['region']['avgDailyIncomeInUSD']
    res['dollarsInFlight'] = int(dollars_in_flight / converted_time)
    return res


def estimator(data):
    # convert time
    converted_time = data['timeToElapse']
    if data['periodType'] == 'weeks':
        converted_time = converted_time * 7
    elif data['periodType'] == 'months':
        converted_time = converted_time * 30
    impact = calculate_estimate(data, converted_time=converted_time)
    severe_impact = calculate_estimate(
        data, converted_time=converted_time, level='severImpact')
    result = {
        'data': data,
        'impact': impact,
        'severeImpact': severe_impact
    }
    return result
