#!/usr/bin/env python

import datetime
import random

class Request:
    timestamp = None
    email = None
    name = None
    selection = None

    def __init__(self, timestamp, email, name, selection):
        self.timestamp = timestamp
        self.email = email
        self.name = name
        self.selection = selection

    def same_person(self, req):
        if self.email == req.email:
            return True
        if self.name == req.name:
            return True
        return False

def read_request_tsv(filepath):
    requests = []
    with open(filepath, 'r') as f:
        for line in f:
            fields = line.split('\t')
            if fields[0] == "Timestamp":
                continue
            requests.append(
                    Request(fields[0], fields[1], fields[2], fields[3]))
    return requests

def read_points_tsv(filepath):
    points = {}
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.split('\t')
            name = fields[0]
            point = int(fields[1])
            if name in points.keys():
                print "Same name in points file %s!" % filepath
                exit(1)
            points[name] = point
    return points

def battle_requests(requests, points):
    winner = 0

    pts = []
    for r in requests:
        pts.append(points[r.name])
    spts = sorted(pts)
    if spts[-1] == spts[-2]:
        random.seed(datetime.datetime.now())
        winner = random.randint(0, len(requests) - 1)
    else:
        winner = pts.index(spts[-1])

    return requests[winner]

if __name__ == "__main__":
    requests = read_request_tsv("request.tsv")
    points = read_points_tsv("points.tsv")

    by_selection = {}
    for r in requests:
        if not r.selection in by_selection.keys():
            by_selection[r.selection] = []
        by_selection[r.selection].append(r)

    final_assignments = []
    for s in by_selection.keys():
        reqs = by_selection[s]
        if len(reqs) == 0:
            continue
        winner = reqs[0]
        if len(reqs) > 1:
            winner = battle_requests(reqs, points)
        final_assignments.append(winner.name + ": " + winner.selection)

    for a in sorted(final_assignments):
        print a
