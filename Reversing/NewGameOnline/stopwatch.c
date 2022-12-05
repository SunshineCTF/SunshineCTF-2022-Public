//
//  stopwatch.c
//
//  Created by Kevin Colley on 9/27/21.
//

#include "stopwatch.h"
#include <string.h>
#include <time.h>
#include <stdio.h>

static inline double timespec_to_double(const struct timespec* ts) {
	return (double)ts->tv_sec + 1.0e-9 * ts->tv_nsec;
}

static inline double current_time(void) {
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	
	return timespec_to_double(&ts);
}

static inline double time_since(double old) {
	return current_time() - old;
}

void Stopwatch_start(Stopwatch* sw) {
	memset(sw, 0, sizeof(*sw));
	sw->last_time = sw->start_time = current_time();
}

bool Stopwatch_hasStarted(Stopwatch* sw) {
	return !!sw->start_time;
}

double Stopwatch_elapsed(const Stopwatch* sw) {
	double now = current_time();
	double elapsed = now - sw->last_time;
	elapsed -= sw->skipped;
	if(sw->is_paused) {
		elapsed -= now - sw->pause_time;
	}
	
	return elapsed;
}

double Stopwatch_tick(Stopwatch* sw) {
	double ret = Stopwatch_elapsed(sw);
	Stopwatch_reset(sw);
	return ret;
}

double Stopwatch_totalTime(const Stopwatch* sw) {
	return time_since(sw->start_time) - sw->skipped;
}

void Stopwatch_reset(Stopwatch* sw) {
	sw->is_paused = false;
	sw->skipped = 0.0;
	sw->last_time = current_time();
}

void Stopwatch_pause(Stopwatch* sw) {
	if(!sw->is_paused) {
		sw->pause_time = current_time();
		sw->is_paused = true;
	}
}

void Stopwatch_resume(Stopwatch* sw) {
	if(sw->is_paused) {
		sw->skipped += time_since(sw->pause_time);
		sw->is_paused = false;
	}
}

bool Stopwatch_isPaused(const Stopwatch* sw) {
	return sw->is_paused;
}
