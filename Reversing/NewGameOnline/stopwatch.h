//
//  stopwatch.h
//
//  Created by Kevin Colley on 9/27/21.
//

#ifndef STOPWATCH_H
#define STOPWATCH_H

#include <stdbool.h>

typedef struct Stopwatch Stopwatch;
struct Stopwatch {
	double start_time;
	double last_time;
	double pause_time;
	double skipped;
	bool is_paused;
};

void Stopwatch_start(Stopwatch* sw);
bool Stopwatch_hasStarted(Stopwatch* sw);
double Stopwatch_elapsed(const Stopwatch* sw);
double Stopwatch_tick(Stopwatch* sw);
double Stopwatch_totalTime(const Stopwatch* sw);
void Stopwatch_reset(Stopwatch* sw);
void Stopwatch_pause(Stopwatch* sw);
void Stopwatch_resume(Stopwatch* sw);
bool Stopwatch_isPaused(const Stopwatch* sw);

#endif /* STOPWATCH_H */
