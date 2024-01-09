#!/usr/bin/env python3
import sqlite3
import time
import datetime


# Object based on meter id
class UtilityMeter:
    def __init__(self, mId, mType, mEpoch, mConsumption, dbConn):
        self.mId = mId
        self.mType = mType
        self.mEpoch = mEpoch
        self.mConsumption = mConsumption
        #
        self.time1 = mEpoch
        self.consumption1 = mConsumption
        self.time2 = mEpoch
        self.consumption2 = mConsumption
        #
        self.dbConn = dbConn


class ElectricMeter(UtilityMeter):
    def getCurrentWatts(self, currTime, currConsumption):
        # Time
        self.time = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.watts = 0
        self.time2 = currTime
        self.consumption2 = currConsumption

        self.timeDiff = self.time2 - self.time1
        if self.timeDiff < 0:
            print(
                "Error: Time Diff Negative. Customer: %s. %d - %d = %d"
                % (self.mId, self.time2, self.time1, self.timeDiff)
            )
        # Min 5min granularity
        if self.timeDiff >= 300:
            # Figure out the power used in this time
            self.powerDiff = self.consumption2 - self.consumption1
            # If the power hasn't incremented, do nothing
            if self.powerDiff != 0:
                # Reset time1 and consumption1
                self.time1 = currTime
                self.consumption1 = currConsumption

                # Convert power diff from kwh to kws
                self.watts = self.powerDiff * 3600 / self.timeDiff
                # If numbers are way out of range, throw an error
                if self.watts > 10000 or self.watts < -10000:
                    print("Calculated use out of range! Got:")
                    print(
                        "[%s] Customer %s Using %f watts. %d Wh / %d s"
                        % (
                            self.time,
                            self.mId,
                            self.watts,
                            self.powerDiff,
                            self.timeDiff,
                        )
                    )
                    return -1

                print(
                    "[%s] Customer %s Using %f watts. %d Wh / %d s"
                    % (self.time, self.mId, self.watts, self.powerDiff, self.timeDiff)
                )

                # Write to db
                self.dbConn.execute(
                    "INSERT INTO utilities(mId, mType, mTime, mTotalConsumption, mConsumed) VALUES (?, ?, ?, ?, ?)",
                    (
                        self.mId,
                        int(self.mType),
                        int(currTime),
                        int(currConsumption),
                        self.watts,
                    ),
                )

        return self.watts


class GasMeter(UtilityMeter):
    def getGasPerSec(self, currTime, currConsumption):
        # Time
        self.time = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.gasPerSec = 0
        self.time2 = currTime
        self.consumption2 = currConsumption

        self.timeDiff = self.time2 - self.time1
        if self.timeDiff < 0:
            print(
                "Error: Time Diff Negative. Customer: %s. %d - %d = %d"
                % (self.mId, self.time2, self.time1, self.timeDiff)
            )
        # Min 5min granularity
        if self.timeDiff >= 300:
            # Calculate gas per second
            self.gasDiff = self.consumption2 - self.consumption1
            # If it hasn't changed, do nothing
            if self.gasDiff != 0:
                # Reset time1 and consumption1
                self.time1 = currTime
                self.consumption1 = currConsumption

                self.gasPerSec = self.gasDiff / self.timeDiff
                # If numbers are way out of range, throw an error
                if self.gasPerSec > 10000 or self.gasPerSec < -10000:
                    print("Calculated use out of range! Got:")
                    print(
                        "[%s] Customer %s Using %f cubic feet / sec. %d / %d s"
                        % (
                            self.time,
                            self.mId,
                            self.gasPerSec,
                            self.gasDiff,
                            self.timeDiff,
                        )
                    )
                    return -1

                print(
                    "[%s] Customer %s Using %f cubic feet / sec. %d / %d s"
                    % (self.time, self.mId, self.gasPerSec, self.gasDiff, self.timeDiff)
                )

                # Write to db
                self.dbConn.execute(
                    "INSERT INTO utilities(mId, mType, mTime, mTotalConsumption, mConsumed) VALUES (?, ?, ?, ?, ?)",
                    (
                        int(self.mId),
                        int(self.mType),
                        int(currTime),
                        int(currConsumption),
                        self.gasPerSec,
                    ),
                )

        return self.gasPerSec


class WaterMeter(UtilityMeter):
    def getWaterPerSec(self, currTime, currConsumption):
        # Time
        self.time = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.waterPerSec = 0
        self.time2 = currTime
        self.consumption2 = currConsumption

        self.timeDiff = self.time2 - self.time1
        if self.timeDiff < 0:
            print(
                "Error: Time Diff Negative. Customer: %s. %d - %d = %d"
                % (self.mId, self.time2, self.time1, self.timeDiff)
            )
        # Min 5min granularity
        if self.timeDiff >= 300:
            # Calculate water per second
            self.waterDiff = self.consumption2 - self.consumption1
            # If it hasn't changed, do nothing
            if self.waterDiff != 0:
                # Reset time1 and consumption1
                self.time1 = currTime
                self.consumption1 = currConsumption

                self.waterPerSec = self.waterDiff / self.timeDiff
                # If numbers are way out of range, throw an error
                if self.waterPerSec > 10000 or self.waterPerSec < -10000:
                    print("Calculated use out of range! Got:")
                    print(
                        "[%s] Customer %s Using %f cubic feet / sec. %d / %d s"
                        % (
                            self.time,
                            self.mId,
                            self.waterPerSec,
                            self.waterDiff,
                            self.timeDiff,
                        )
                    )
                    return -1

                print(
                    "[%s] Customer %s Using %f cubic feet / sec. %d / %d s"
                    % (
                        self.time,
                        self.mId,
                        self.waterPerSec,
                        self.waterDiff,
                        self.timeDiff,
                    )
                )

                # Write to db
                self.dbConn.execute(
                    "INSERT INTO utilities(mId, mType, mTime, mTotalConsumption, mConsumed) VALUES (?, ?, ?, ?, ?)",
                    (
                        int(self.mId),
                        int(self.mType),
                        int(currTime),
                        int(currConsumption),
                        self.waterPerSec,
                    ),
                )

        return self.waterPerSec


def main():
    # SQLite connection and cursor creation
    conn = sqlite3.connect("/data/metermaid.db")
    cursor = conn.cursor()

    # Example usage of ElectricMeter class
    electric_meter = ElectricMeter(1, "electric", time.time(), 1000, cursor)
    electric_meter.getCurrentWatts(time.time(), 1500)

    # Example usage of GasMeter class
    gas_meter = GasMeter(2, "gas", time.time(), 50, cursor)
    gas_meter.getGasPerSec(time.time(), 100)

    # Example usage of WaterMeter class
    water_meter = WaterMeter(3, "water", time.time(), 200, cursor)
    water_meter.getWaterPerSec(time.time(), 300)

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
