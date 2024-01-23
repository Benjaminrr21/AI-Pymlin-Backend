from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from random import random

import json

from .AIgame import minimax, alphabetaM,alphabetaH

DEPTH_EASY = 3
DEPTH_MEDIUM = 4
DEPTH_HARD = 4

@csrf_exempt
def make_move(request):
    try:
        state = json.loads(request.body)
        difficulty = state['difficulty'] # DEPTH
        player = state['player']
        line_made = state['line_made']    # existing code

    except Exception as e:
        print(f"Error in make_move: {str(e)}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    


       # return JsonResponse({ 'move': ['set', -1, x, y] })
    

    if difficulty == 'easy':
        _, move = minimax(state, DEPTH_EASY, player, line_made)
    elif difficulty == 'medium':
        _, move = alphabetaM(state, DEPTH_MEDIUM, -100000, 100000, player, line_made)
    elif difficulty == 'hard':
        _, move = alphabetaH(state, DEPTH_HARD, -100000, 100000, player, line_made)
    
    return JsonResponse({ 'move': move })