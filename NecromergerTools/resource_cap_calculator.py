import tkinter as tk

from pydantic import BaseModel, computed_field


class ResourceAttributes(BaseModel):
    base_subtotal: int
    servo_bonus: int
    using_servo: bool
    base_modifier: int
    relic_modifer: int
    using_relic: bool

    @computed_field # type: ignore[prop-decorato
    @property
    def subtotal(self) -> int:
        subtotal = self.base_subtotal
        if self.using_servo:
            subtotal += self.servo_bonus
        return subtotal
    
    @computed_field # type: ignore[prop-decorato
    @property
    def modifier(self) -> float:
        modifier = self.base_modifier
        if self.using_relic:
            modifier += self.relic_modifer
        return modifier
    
    @computed_field # type: ignore[prop-decorato
    @property
    def total(self) -> int:
        return int(self.subtotal * (1+self.modifier/100))

# def create_resoucrce_frame(master, resouce_label: str) -> None:
#     frame = tk.Frame(master, width=200, height=400)

#     tk.Label(frame, text=resouce_label).pack()
#     tk.Label(frame, text="Base Subtotal:")
#     tk.Entry(frame).pack()
#     tk.Label(frame, text="Base Modifier")
#     tk.Entry(frame)
#     tk.Label(frame, text="Using Relic:")
#     tk.Checkbutton(frame)
#     tk.Label(frame, text="Relic Modifier:")
#     tk.Entry(frame)


# def main() -> None:
#     root = tk.Tk()
#     root.title("Resource Cap Calculator")
#     root.geometry("800x600+50+50")

#     tk.Label(root, text="Mana", font=("Font", 20)).pack()
#     tk.Label(root, text="Base Subtotal:").pack()
#     tk.Entry(root).pack()
#     tk.Label(root, text="Base Modifier").pack()
#     tk.Entry(root).pack()
#     tk.Label(root, text="Using Relic:").pack()
#     tk.Checkbutton(root).pack()
#     tk.Label(root, text="Relic Modifier:").pack()
#     tk.Entry(root).pack()
    


#     root.mainloop()

if __name__ == "__main__":
    main()
