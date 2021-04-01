class Election:
    # does instant runoff election

    def __init__(self, routes: list):
        self.routes = routes

    def rank_routes(self, voters: list) -> dict:
        # counts the votes for each route
        prel_result = {route: 0 for route in self.routes}
        for voter in voters:
            prel_result[voter.ranking[0]] += 1

        return prel_result

    @staticmethod
    def find_last_place(prel_result: dict, voters: list) -> str:
        # finds out which route is the least voted on (and handles last place ties)
        least_votes = len(voters)+1
        last_places = []
        for route in prel_result:
            if prel_result[route] < least_votes:
                last_places = [route]
                least_votes = prel_result[route]
            elif prel_result[route] == least_votes:
                last_places += [route]

        if len(last_places) > 1:
            raise NotImplementedError('resolve ties')
        else:
            last_place = last_places[0]

        return last_place

    def prune_last_place(self, last_place: str, voters: list) -> dict:
        # prunes the route with the least votes from the routes list and from all the voters rankings
        self.routes.remove(last_place)
        for voter in voters:
            voter.ranking.remove(last_place)

        return self.rank_routes(voters)

    def find_winner(self, voters) -> str:
        # declares which route won the vote by using instant run-off voting
        prel_result = self.rank_routes(voters)

        while len(prel_result) > 1:
            last_place = self.find_last_place(prel_result, voters)
            prel_result = self.prune_last_place(last_place, voters)

        winner = list(prel_result.keys())[0]
        print(winner + ' got the most votes!')

        return winner