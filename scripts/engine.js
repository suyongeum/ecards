class Selection {
    constructor () {
        const content   = document.querySelector('.db').innerHTML;
        this.data = JSON.parse(content);
        this.max  = 2075;
        this.id   = 3;
        this.word = 'ability';        
        this.wordObj = {};
    }

    getRandomInt() {
        return Math.floor(Math.random() * this.max);
    }

    randomSelection() {
        this.id   = this.getRandomInt();
        return this.id;
    }    

    getWord() {
        this.id   = this.getRandomInt();
        this.word = (this.data[this.id])['word'];
        return this.word;
    }

    getObject() {
        this.id      = this.getRandomInt();
        this.wordObj = this.data[this.id];
        return this.wordObj;
    }
}

const selection = new Selection();
