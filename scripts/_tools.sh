BLUE='\033[0;34m'
NC='\033[0m' # No Color

function msg() {
    echo -e "${BLUE}=> $@${NC}\n"
}
