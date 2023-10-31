import { Button } from "@mui/material";

type UpdateProps = {
  setUpdateClicked: React.Dispatch<React.SetStateAction<boolean>>;
};

export function Update({ setUpdateClicked }: UpdateProps) {
  const handleUpdateClicked = () => {
    setUpdateClicked(true);
  };
  return (
    <Button
      variant="outlined"
      onClick={handleUpdateClicked}
      sx={{ width: "fit-content", backgroundColor: "#30115c", color: "white" }}
    >
      Update
    </Button>
  );
}
