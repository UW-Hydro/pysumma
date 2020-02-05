from sklearn.metrics import mean_absolute_error, mean_squared_error
import math


class Validation(object):

    def analysis(observation, simulation):
        MAE_B = mean_absolute_error(observation, simulation)
        MSE_B = mean_squared_error(observation, simulation)
        RMSE_B = math.sqrt(MSE_B)
        print('Mean Absolute Error: %f' % MAE_B)
        print('Mean Squared Error: %f' % MSE_B)
        print('Root Mean Squared Error: %f' % RMSE_B)
