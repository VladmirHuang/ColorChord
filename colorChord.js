class _Note {
    static NOTES = ["A", "D", "G", "C", "F", "Bb", "Eb", "Ab", "Db", "Fsharp", "B", "E"]
    constructor(name) {
        this.name = name;
        if (name == "A") {
            this.index = 1;
        } else if (name == "D") {
            this.index = 2;
        } else if (name == "G") {
            this.index = 3;
        } else if (name == "C" || name == "B#" || name == "Bsharp") {
            this.index = 4;
        } else if (name == "F" || name == "E#" || name == "Esharp") {
            this.index = 5;
        } else if (name == "Bb" || name == "A#" || name == "Asharp") {
            this.index = 6;
        } else if (name == "Eb" || name == "D#" || name == "Dsharp") {
            this.index = 7;
        } else if (name == "Ab" || name == "G#" || name == "Gsharp") {
            this.index = 8;
        } else if (name == "Db" || name == "C#" || name == "Csharp") {
            this.index = 9;
        } else if (name == "Fsharp" || name == "Gb" || name == "F#") {
            this.index = 10;
        } else if (name == "B" || name == "Cb") {
            this.index = 11;
        } else if (name == "E" || name == "Fb") {
            this.index = 12;
        } else {
            throw new Error(`无效的音符名：${name}`);
        }
    }
    static abs(x) {
        return x >= 0 ? x : -x;
    }
    angle() {
            /*
             * 计算向量与 x 轴的夹角（单位：度）
             * :return: float
             */
            return (this.index * Math.PI / 6 - Math.PI / 12);
        }
        //计算从自身逆时针到other的纯五跨度数
    perfect5num2other(other) {
        if (other.index == this.index) {
            return 0;
        } else {
            interval = other.index - self.index;
            if (interval > 0) {
                return interval;
            } else {
                return interval + 12;
            }
        }
    }

    equal_to(other) {
        return this.index == other.index;
    }

    //返回逆时针方向第n个音符_Note
    next(n) {
        let new_ind = this.index + n;
        if (n > 0) {
            if (new_ind > 12) {
                new_ind -= 12;
            }

        } else {
            if (new_ind <= 0) {
                new_ind += 12;
            }
        }
        return new _Note(_Note.NOTES[new_ind - 1])
    }
    lt(other) {
        /*
       * 小于
       *
:param other: _Note实例
:return: */
        return this.index < other.index;
    }
    gt(other) {
        /*
         * 大于
         * :param other: _Note实例
         * :return:
         */
        return this.index > other.index;
    }
}

class Chord {
    constructor(notes, name = null) {
        if (notes.length === 0) {
            throw new Error("没有输入音符");
        }
        this.name = name;
        this.temp_theta = null;
        this.notes = [];
        notes.forEach((note) => {
            this.notes.push(new _Note(note));
        });
        this.notes.sort((a, b) => (a.lt(b) ? -1 : a.gt(b) ? 1 : 0));
    }
}